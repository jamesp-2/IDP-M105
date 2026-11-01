"""Storage-rack occupancy and junction classification."""
from motors import *
import time
import sensors


# Compass directions
N = 0
E = 1
S = 2
W = 3

# Common route templates
paths = {
    "right pickup 1": ["straight", "left", "left into pickup"],
    "right pickup 2": ["straight", "left", "straight", "left into pickup"],
    "left pickup 1": ["straight", "right", "right into pickup"],
    "left pickup 2": ["straight", "right", "straight", "right into pickup"],
    "bottom right return": ["straight", "straight", "right", "straight", "straight"],
    "bottom left return": ["straight", "straight", "left", "straight", "straight"],
    "top right return": ["straight", "right"],
    "top left return": ["straight", "left"]
}

task_list = ["right pickup 1",
            "left pickup 1",
            "right pickup 2",
            "left pickup 2"]

class route:
    """Store and extend one pickup, delivery, and return route."""

    def __init__(self, pickup_path):
        self.pickup_path = pickup_path
        self.sel_route = []
        self.floor = 0

    def __repr__(self):
        """Return the selected route as a readable value."""
        return f"route = {self.sel_route}"

    def start_route(self):
        """Start the route using its pickup sequence."""
        self.sel_route = list(self.pickup_path)
        return self.sel_route

    def delivery_pathfinding(self):
        """Add delivery steps based on the pickup path and magnetic reading."""
        # Route outbound to the target rack
        if self.pickup_path == paths.get("right pickup 1"):
            if sensors.get_magnetic_reading() == "N":
                self.floor = 1
                self.sel_route.extend(["left", "right", "straight", "right", "straight"])
                self.target_rack = top_right_rack
                for _ in range(top_right_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("right into delivery")
            elif sensors.get_magnetic_reading() == "S":
                self.sel_route.extend(["right", "straight"])
                self.target_rack = bottom_right_rack
                for _ in range(bottom_right_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("left into delivery")
            else:
                self.sel_route.extend(["left", "right", "straight"])

        elif self.pickup_path == paths.get("right pickup 2"):
            if sensors.get_magnetic_reading() == "N":
                self.floor = 1
                self.sel_route.extend(["left", "straight", "right", "straight", "right", "straight"])
                self.target_rack = top_right_rack
                for _ in range(top_right_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("right into delivery")
            elif sensors.get_magnetic_reading() == "S":
                self.target_rack = bottom_right_rack
                self.sel_route.append("right")
                for _ in range(bottom_right_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("left into delivery")
            else:
                self.sel_route.extend(["left", "straight", "right", "straight"])

        elif self.pickup_path == paths.get("left pickup 1"):
            if sensors.get_magnetic_reading() == "N":
                self.floor = 1
                self.sel_route.extend(["right", "left", "straight", "left", "straight"])
                self.target_rack = top_left_rack
                for _ in range(top_left_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("left into delivery")
            elif sensors.get_magnetic_reading() == "S":
                self.sel_route.extend(["left", "straight"])
                self.target_rack = bottom_left_rack
                for _ in range(bottom_right_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("right into delivery")
            else:
                self.sel_route.extend(["right", "left", "straight"])

        elif self.pickup_path == paths.get("left pickup 2"):
            if sensors.get_magnetic_reading() == "N":
                self.floor = 1
                self.sel_route.extend(["right", "straight", "left", "straight", "left", "straight"])
                self.target_rack = top_left_rack
                for _ in range(top_left_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("left into delivery")
            elif sensors.get_magnetic_reading() == "S":
                self.sel_route.extend(["left", "straight"])
                self.target_rack = bottom_left_rack
                for _ in range(bottom_right_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("right into delivery")
            else:
                self.sel_route.extend(["right", "left", "straight"])

    def return_pathfinding(self):
        """Append the return path based on the delivery floor and direction."""
        if self.floor == 1:
            if self.sel_route[-1] == "right into delivery":
                self.sel_route.append("right")
                for _ in range(top_right_rack.first_available_slot() - 1):
                    self.sel_route.append("straight")
                self.sel_route.extend(paths["top right return"])
            elif self.sel_route[-1] == "left into delivery":
                self.sel_route.append("left")
                for _ in range(top_left_rack.first_available_slot() - 1):
                    self.sel_route.append("straight")
                self.sel_route.extend(paths["top left return"])
        else:
            if self.sel_route[-1] == "right into delivery":
                self.sel_route.append("right")
                for _ in range(bottom_left_rack.first_available_slot() - 1):
                    self.sel_route.append("straight")
                self.sel_route.extend(paths["bottom left return"])
            elif self.sel_route[-1] == "left into delivery":
                self.sel_route.append("left")
                for _ in range(bottom_right_rack.first_available_slot() - 1):
                    self.sel_route.append("straight")
                self.sel_route.extend(paths["bottom right return"])

    def box_in_slot(self):
        """Check whether the target slot is full and reroute if needed."""
        import sensors
        import main

        # Mark the slot as filled if the object is detected
        x = 10
        dist = sensors.get_distance()

        if dist is not None and dist < x:
            if hasattr(self, "target_rack"):
                current_slot = self.target_rack.first_available_slot()
                self.target_rack.slot_is_full(current_slot)
                delivery_turn = self.sel_route[main.route_counter - 1]
                self.sel_route = self.sel_route[: main.route_counter]
                self.sel_route.extend(["straight", delivery_turn])
                self.return_pathfinding()
            return 1
        return 0


class rack():
    """Track the free and occupied slots for one rack location."""

    def __init__(self, side, floor, slt_list):
        self.side = side
        self.floor = floor
        self.slt_list = slt_list
        self.next_free_slot = self.first_available_slot()

    def __repr__(self):
        """Return a readable rack description."""
        return f"Rack(side={self.side}, floor={self.floor}, slt_list={self.slt_list})"

    def first_available_slot(self):
        """Return the first empty slot, or -1 if all slots are occupied."""
        for i in range(len(self.slt_list)):
            if self.slt_list[i] == 0:
                return i
        return -1

    def slot_is_full(self, slot_index):
        """Mark a slot occupied and update the cached free slot."""
        if not 0 <= slot_index < len(self.slt_list):
            raise IndexError("Slot index is outside this rack.")

        if self.slt_list[slot_index] == 0:
            self.slt_list[slot_index] = 1
            self.next_free_slot = self.first_available_slot()
            return True
        else:
            print(f"Slot {slot_index} is already full.")
            return False


class node():
    """Classify a junction from the initial and follow-up sensor samples."""

    def __init__(self, line_sensor_list):
        self.line_sensor_list = line_sensor_list

    def __repr__(self):
        """Return a readable node description."""
        return f"Node(line_sensor_list={self.line_sensor_list})"

    def decide_node_type(self, read_sensors):
        """Advance to the junction and classify it from a fresh sensor sample."""
        first_reading = self.line_sensor_list
        outer_first_reading = [first_reading[0], first_reading[-1]]

        if outer_first_reading not in ([1, 1], [1, 0], [0, 1]):
            return None

        bot.stop()
        start = time.time()
        while time.time() - start < 0.4:
            bot.forward(30)
        second_reading = read_sensors()
        inner_second_reading = [second_reading[1], second_reading[2]]

        if outer_first_reading == [1, 1]:
            if inner_second_reading == [0, 0]:
                return "T junction"
            elif inner_second_reading == [1, 1]:
                return "Cross junction"
        elif outer_first_reading == [1, 0]:
            if inner_second_reading == [0, 0]:
                return "Left turn"
            elif inner_second_reading == [1, 1]:
                return "Left T junction"
        elif outer_first_reading == [0, 1]:
            if inner_second_reading == [0, 0]:
                return "Right turn"
            elif inner_second_reading == [1, 1]:
                return "Right T junction"


# Rack occupancy state for each storage area
top_left_rack = rack("left", "top", [0, 0, 0, 0, 0, 0])
bottom_left_rack = rack("left", "bottom", [0, 0, 0, 0, 0, 0])
top_right_rack = rack("right", "top", [0, 0, 0, 0, 0, 0])
bottom_right_rack = rack("right", "bottom", [0, 0, 0, 0, 0, 0])

# Direction map from the start position
path_from_start = {
    "P1": [E, E, N],
    "P2": [E, E, N, N],
    "P3": [W, W, N],
    "P4": [W, W, N, N],
    "BL1": [E, E, N, N],
    "TR": [N, N],
    "BR1": [E, E, N, N],
}

pick_up_locations = ["P1", "P2", "P3", "P4"]
current_selection = 0
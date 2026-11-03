"""Storage-rack occupancy and junctiOn classificatiOn."""
import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

import old_main
from old_motors import *
import time
import old_sensors
import old_leds
led = old_leds.LED()
led.start()

# Compass directiOns
N = 0
E = 1
S = 2
W = 3

# CommOn route templates
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

task_list = ["left pickup 1",
            "right pickup 1",
            "left pickup 2",
            "right pickup 2"]

class route:
    """Store and extend pickup, delivery, and return route."""

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
        """Add delivery steps based On the pickup path and magnetic reading."""
        # Route outbound to the target rack
        if self.pickup_path == paths.get("right pickup 1"):
            if old_sensors.get_magnetic_reading() == "N":
                led.red.value(old_leds.On)
                led.yellow.value(old_leds.Off)
                led.green.value(old_leds.Off)
                self.floor = 1
                self.sel_route.extend(["left", "right", "straight", "right", "straight"])
                self.target_rack = top_right_rack
                self.target_slot = self.target_rack.first_available_slot()
                for _ in range(self.target_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("right into delivery")
            elif old_sensors.get_magnetic_reading() == "S":
                led.red.value(old_leds.Off)
                led.yellow.value(old_leds.Off)
                led.green.value(old_leds.On)
                self.sel_route.extend(["right", "straight"])
                self.target_rack = bottom_right_rack
                self.target_slot = self.target_rack.first_available_slot()
                for _ in range(self.target_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("left into delivery")
            else:
                self.sel_route.extend(["left", "right", "straight"])

        elif self.pickup_path == paths.get("right pickup 2"):
            if old_sensors.get_magnetic_reading() == "N":
                led.red.value(old_leds.On)
                led.yellow.value(old_leds.Off)
                led.green.value(old_leds.Off)
                self.floor = 1
                self.sel_route.extend(["left", "straight", "right", "straight", "right", "straight"])
                self.target_rack = top_right_rack
                self.target_slot = self.target_rack.first_available_slot()
                for _ in range(self.target_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("right into delivery")
            elif old_sensors.get_magnetic_reading() == "S":
                led.red.value(old_leds.Off)
                led.yellow.value(old_leds.Off)
                led.green.value(old_leds.On)
                self.target_rack = bottom_right_rack
                self.target_slot = self.target_rack.first_available_slot()
                self.sel_route.append("right")
                for _ in range(self.target_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("left into delivery")
            else:
                self.sel_route.extend(["left", "straight", "right", "straight"])

        elif self.pickup_path == paths.get("left pickup 1"):
            if old_sensors.get_magnetic_reading() == "N":
                led.red.value(old_leds.On)
                led.yellow.value(old_leds.Off)
                led.green.value(old_leds.Off)
                self.floor = 1
                self.sel_route.extend(["right", "left", "straight", "left", "straight"])
                self.target_rack = top_left_rack
                self.target_slot = self.target_rack.first_available_slot()
                for _ in range(self.target_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("left into delivery")
            elif old_sensors.get_magnetic_reading() == "S":
                led.red.value(old_leds.Off)
                led.yellow.value(old_leds.Off)
                led.green.value(old_leds.On)
                self.sel_route.extend(["left", "straight"])
                self.target_rack = bottom_left_rack
                self.target_slot = self.target_rack.first_available_slot()
                for _ in range(self.target_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("right into delivery")
            else:
                self.sel_route.extend(["right", "left", "straight"])

        elif self.pickup_path == paths.get("left pickup 2"):
            if old_sensors.get_magnetic_reading() == "N":
                led.red.value(old_leds.On)
                led.yellow.value(old_leds.Off)
                led.green.value(old_leds.Off)
                self.floor = 1
                self.sel_route.extend(["right", "straight", "left", "straight", "left", "straight"])
                self.target_rack = top_left_rack
                self.target_slot = self.target_rack.first_available_slot()
                for _ in range(self.target_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("left into delivery")
            elif old_sensors.get_magnetic_reading() == "S":
                led.red.value(old_leds.Off)
                led.yellow.value(old_leds.Off)
                led.green.value(old_leds.On)
                self.sel_route.extend(["left", "straight"])
                self.target_rack = bottom_left_rack
                self.target_slot = self.target_rack.first_available_slot()
                for _ in range(self.target_rack.first_available_slot()):
                    self.sel_route.append("straight")
                self.sel_route.append("right into delivery")
            else:
                self.sel_route.extend(["right", "left", "straight"])

    def return_pathfinding(self):
        """Append the return path based On the delivery floor and direction."""
        if self.floor == 1:
            if self.sel_route[-1] == "right into delivery":
                self.sel_route.append("right")
                for _ in range(self.target_rack.first_available_slot() - 1):
                    self.sel_route.append("straight")
                self.sel_route.extend(paths["top right return"])
            elif self.sel_route[-1] == "left into delivery":
                self.sel_route.append("left")
                for _ in range(self.target_rack.first_available_slot() - 1):
                    self.sel_route.append("straight")
                self.sel_route.extend(paths["top left return"])
        else:
            if self.sel_route[-1] == "right into delivery":
                self.sel_route.append("right")
                for _ in range(self.target_rack.first_available_slot() - 1):
                    self.sel_route.append("straight")
                self.sel_route.extend(paths["bottom left return"])
            elif self.sel_route[-1] == "left into delivery":
                self.sel_route.append("left")
                for _ in range(self.target_rack.first_available_slot() - 1):
                    self.sel_route.append("straight")
                self.sel_route.extend(paths["bottom right return"])

    def box_in_slot(self):
        """Check whether the target slot is full and reroute if needed."""

        # Mark the slot as filled if the object is detected
        x = 150
        dist = old_sensors.get_distance()

        if dist is not None and dist < x:
            if hasattr(self, "target_rack"):
                current_slot = self.target_rack.first_available_slot()
                self.target_rack.slot_is_full(current_slot)
                delivery_turn = self.sel_route[old_main.route_counter - 1]
                self.sel_route = self.sel_route[: old_main.route_counter]
                self.sel_route.extend(["straight", delivery_turn])
                self.return_pathfinding()
                print(self.target_rack.first_available_slot())
            return 1
        return 0


class rack():
    """Track the free and occupied slots for One rack locatiOn."""

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
    """Classify a junctiOn from the initial and follow-up sensor samples."""

    def __init__(self, line_sensor_list):
        self.line_sensor_list = line_sensor_list

    def __repr__(self):
        """Return a readable node descriptiOn."""
        return f"Node(line_sensor_list={self.line_sensor_list})"

    def decide_node_type(self, read_sensors):
        """Advance to the junctiOn and classify it from a fresh sensor sample."""
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
                return "T junctiOn"
            elif inner_second_reading == [1, 1]:
                return "Cross junctiOn"
        elif outer_first_reading == [1, 0]:
            if inner_second_reading == [0, 0]:
                return "Left turn"
            elif inner_second_reading == [1, 1]:
                return "Left T junctiOn"
        elif outer_first_reading == [0, 1]:
            if inner_second_reading == [0, 0]:
                return "Right turn"
            elif inner_second_reading == [1, 1]:
                return "Right T junctiOn"


# Rack occupancy state for each storage area
top_left_rack = rack("left", "top", [0, 0, 0, 0, 0, 0])
bottom_left_rack = rack("left", "bottom", [0, 0, 0, 0, 0, 0])
top_right_rack = rack("right", "top", [0, 0, 0, 0, 0, 0])
bottom_right_rack = rack("right", "bottom", [0, 0, 0, 0, 0, 0])

# DirectiOn map from the start positiOn
path_from_start = {
    "P1": [E, E, N],
    "P2": [E, E, N, N],
    "P3": [W, W, N],
    "P4": [W, W, N, N],
    "BL1": [E, E, N, N],
    "TR": [N, N],
    "BR1": [E, E, N, N],
}

pick_up_locatiOns = ["P1", "P2", "P3", "P4"]
current_selectiOn = 0




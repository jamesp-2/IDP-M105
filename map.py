# Represents a storage rack that tracks which slots are free or occupied.
class rack():
    """Track the occupied and available storage slots in one rack."""

    def __init__(self, side, floor, slt_list):
        # Store the rack's position and slot states
        # (0 = empty, 1 = occupied).
        self.side = side
        self.floor = floor
        self.slt_list = slt_list
        # Cache the earliest slot that may still be empty to avoid rescanning.
        self.next_free_slot = 0

    def __repr__(self):
        """Return a readable description of this rack."""
        return f"Rack(side={self.side}, floor={self.floor}, slt_list={self.slt_list})"

    def first_available_slot(self):
        """Return the first empty slot's index, or None if the rack is full."""
        # Advance past occupied slots, starting from the cached position.
        while (
            self.next_free_slot < len(self.slt_list)
            and self.slt_list[self.next_free_slot] != 0
        ):
            self.next_free_slot += 1

        # If the cursor reached the end, there are no available slots.
        if self.next_free_slot < len(self.slt_list):
            return self.next_free_slot
        return None

    def slot_is_full(self, slot_index):
        """Mark an empty slot as occupied and report if it was already full."""
        if self.slt_list[slot_index] == 0:
            self.slt_list[slot_index] = 1
            # Keep the cached first-free position current when it is filled.
            if slot_index == self.next_free_slot:
                self.next_free_slot += 1
        else:
            print(f"Slot {slot_index} is already full.")


class node():
    """Store line-sensor readings and classify the detected junction."""

    def __init__(self, line_sensor_list1, line_sensor_list2):
        """Keep the two sensor readings together for junction classification."""
        self.line_sensor_list = [line_sensor_list1, line_sensor_list2]

    def __repr__(self):
        """Return a readable description of this node's sensor readings."""
        return f"Node(line_sensor_list={self.line_sensor_list})"

    def decide_node_type(self, line_sensor_list):
        """Return the junction name that matches the supplied sensor pattern."""
        if line_sensor_list == [[1, 1, 1, 1], [0, 0, 0, 0]]:
            return "T junction"
        elif line_sensor_list == [[1, 1, 1, 1], [0, 1, 1, 0]]:
            return "Cross junction"
        elif line_sensor_list == [[0, 1, 1, 1], [0, 0, 0, 0]]:
            return "Right turn"
        elif line_sensor_list == [[1, 1, 1, 0], [0, 0, 0, 0]]:
            return "Left turn"


# Create one initially empty rack for each corner of the map.
top_left_rack = rack("left", "top", [0, 0, 0, 0, 0, 0])
bottom_left_rack = rack("left", "bottom", [0, 0, 0, 0, 0, 0])
top_right_rack = rack("right", "top", [0, 0, 0, 0, 0, 0])
bottom_right_rack = rack("right", "bottom", [0, 0, 0, 0, 0, 0])

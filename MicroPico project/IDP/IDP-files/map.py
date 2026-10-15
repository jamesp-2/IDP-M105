"""Storage-rack occupancy and line-pattern junction classification."""


class rack():
    """Track the free and occupied slots for one rack location."""

    def __init__(self, side, floor, slt_list):
        # Keep location information and slot states (0 = empty, 1 = occupied).
        self.side = side
        self.floor = floor
        self.slt_list = slt_list
        # Cache the first free slot, or -1 when the rack starts full.
        self.next_free_slot = self.first_available_slot()

    def __repr__(self):
        """Return a readable description of this rack."""
        return f"Rack(side={self.side}, floor={self.floor}, slt_list={self.slt_list})"

    def first_available_slot(self):
        """Return the index of the first empty slot, or -1 if none remain."""
        for i in range(len(self.slt_list)):
            if self.slt_list[i] == 0:
                return i
        return -1

    def slot_is_full(self, slot_index):
        """Mark a slot occupied, returning whether it was previously empty."""
        if not 0 <= slot_index < len(self.slt_list):
            raise IndexError("Slot index is outside this rack.")

        if self.slt_list[slot_index] == 0:
            # Update the cached next slot after changing the occupancy list.
            self.slt_list[slot_index] = 1
            self.next_free_slot = self.first_available_slot()
            return True
        else:
            print(f"Slot {slot_index} is already full.")
            return False


class node():
    """Store two line-sensor samples and classify their junction pattern."""

    def __init__(self, line_sensor_list1, line_sensor_list2):
        """Keep the earlier and later readings in classification order."""
        self.line_sensor_list = [line_sensor_list1, line_sensor_list2]

    def __repr__(self):
        """Return a readable description of this node's sensor readings."""
        return f"Node(line_sensor_list={self.line_sensor_list})"

    def decide_node_type(self, line_sensor_list=None):
        """Return a junction label for a known pair of four-sensor patterns."""
        if line_sensor_list is None:
            line_sensor_list = self.line_sensor_list

        # Match the two observations against the supported junction patterns.
        if line_sensor_list == [[1, 1, 1, 1], [0, 0, 0, 0]]:
            return "T junction"
        elif line_sensor_list == [[1, 1, 1, 1], [0, 1, 1, 0]]:
            return "Cross junction"
        elif line_sensor_list == [[0, 1, 1, 1], [0, 0, 0, 0]]:
            return "Right turn"
        elif line_sensor_list == [[1, 1, 1, 0], [0, 0, 0, 0]]:
            return "Left turn"
        elif line_sensor_list == [[0, 1, 1, 1], [0, 1, 1, 0]]:
            return "Right T junction"
        elif line_sensor_list == [[1, 1, 1, 0], [0, 1, 1, 0]]:
            return "Left T junction"
        return None


# Initialize six empty slots for each of the four rack locations.
top_left_rack = rack("left", "top", [0, 0, 0, 0, 0, 0])
bottom_left_rack = rack("left", "bottom", [0, 0, 0, 0, 0, 0])
top_right_rack = rack("right", "top", [0, 0, 0, 0, 0, 0])
bottom_right_rack = rack("right", "bottom", [0, 0, 0, 0, 0, 0])

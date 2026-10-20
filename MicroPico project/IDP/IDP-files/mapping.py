"""Storage-rack occupancy and line-pattern junction classification."""
from motors import *
import time

N=0
E=1
S=2
W=3

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


# Initialize six empty slots for each of the four rack locations.
top_left_rack = rack("left", "top", [0, 0, 0, 0, 0, 0])
bottom_left_rack = rack("left", "bottom", [0, 0, 0, 0, 0, 0])
top_right_rack = rack("right", "top", [0, 0, 0, 0, 0, 0])
bottom_right_rack = rack("right", "bottom", [0, 0, 0, 0, 0, 0])


#Directions
path_from_start ={
    "P1": [E,E,N],
    "P2": [E,E,N,N],
    "P3": [W,W,N],
    "P4": [W,W,N,N],
    "BL1":[E,E,N,N],
    "TR": [N,N],
    "BR1":[W,W,N,N]
    }

pick_up_locations = ["P1","P2","P3","P4"]
current_selection = 0





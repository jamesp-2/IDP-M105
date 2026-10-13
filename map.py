class rack():
    def __init__(self, side, floor, slt_list):
        self.side = side
        self.floor = floor
        self.slt_list = slt_list

    def first_available_slot(self):
        for i in range(len(self.slt_list)):
            if self.slt_list[i] == 0:
                return i

    def slot_is_full(self, slot_index):
        self.slt_list[slot_index] = 1

top_left_rack = rack("left", "top", [0, 0, 0, 0, 0, 0])
bottom_left_rack = rack("left", "bottom", [0, 0, 0, 0, 0, 0])
top_right_rack = rack("right", "top", [0, 0, 0, 0, 0, 0])
bottom_right_rack = rack("right", "bottom", [0, 0, 0, 0, 0, 0])


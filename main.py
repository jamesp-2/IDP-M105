from config import *

state = "wait_for_start"
box = None

while True:
    if state == "wait_for_start":
        if buttton.value() = 1:
            state = "operate"

    elif state == "operate":
        box = find_box()
        if box is not None:
            state  = "pickup":
        
    elif state == "pickup":
        close_claw()
        lift()
        state = "deliver"

    elif state == "deliver":
        go_to_bay(box)
        lower()
        open_claw()
        box = None
        state = "operate"


"""Top-level robot workflow with hardware-specific steps left explicit."""

import sys
import time

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from claw import close_claw, lift, lower, open_claw
from config import button
from path import *
from mapping import *



def pick_bay(selection):
    return pick_up_locations[selection % len(pick_up_locations)]

    


def go_to_bay(box):
    """Placeholder for routing; the map and route policy are not specified."""
    pass


def main():
    """Wait for start, then repeat the pickup-and-delivery state sequence."""
    state = "wait_for_start"
    selection = 0
    box = None
    current_location = []
    current_direction = N

    while True:
        # Remain idle until the configured start button is pressed.
        if state == "wait_for_start":
            if button.value() == 1:
                state = "operate"

        elif state == "operate":
            # Look for work only after start; the detector is hardware-specific.
            bay = pick_bay(selection)
            follow_path(bay, current_direction, current_location)
            selection+=1
            state = "pickup"

        elif state == "pickup":
            # Secure the detected item and raise it before attempting delivery.
            close_claw()
            lift()
            state = "deliver"

        elif state == "deliver":
            # Navigate to the destination before releasing the item.
            go_to_bay(box)
            lower()
            open_claw()
            box = None
            state = "operate"

        # Yield briefly each iteration instead of continuously busy-spinning.
        time.sleep_ms(20)


# Avoid starting the hardware workflow when this module is imported elsewhere.
if __name__ == "__main__":
    main()

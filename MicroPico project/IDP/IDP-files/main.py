"""Top-level robot workflow with hardware-specific steps left explicit."""

import time

from claw import close_claw, lift, lower, open_claw
from config import button


def find_box():
    """Placeholder for box detection; sensor behavior is not specified."""
    pass


def go_to_bay(box):
    """Placeholder for routing; the map and route policy are not specified."""
    pass


def main():
    """Wait for start, then repeat the pickup-and-delivery state sequence."""
    state = "wait_for_start"
    box = None

    while True:
        # Remain idle until the configured start button is pressed.
        if state == "wait_for_start":
            if button.value() == 1:
                state = "operate"

        elif state == "operate":
            # Look for work only after start; the detector is hardware-specific.
            box = find_box()
            if box is not None:
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

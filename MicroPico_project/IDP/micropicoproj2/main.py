"""Top-level robot workflow with hardware-specific steps left explicit."""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from claw import *
from config import button
from line_correction import *
from mapping import *
from leds import *
from pathing import *
from motors import *
import time

def main():
    """Wait for start, then repeat the pickup-and-delivery state sequence."""
    state = "wait_for_start"

    while True:
        # Remain idle until the configured start button is pressed.
        if state == "wait_for_start":
            if button.value() == 1:

                start_alignment("left")
                lift()
                open_claw()

                while True:
                    led.flash()
                    if current_pickup_index >= len(task_list):
                        bot.stop()
                        break

                    readings = read_line_sensors()
                    print(readings)

                    current_task_name = task_list[current_pickup_index]
                    current_pickup_path = paths.get(current_task_name)
                    print(current_pickup_path)
                    pathing(readings, current_pickup_path)
                    time.sleep_ms(25)

main()
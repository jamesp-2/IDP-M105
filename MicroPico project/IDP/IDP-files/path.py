"""Line-sensor validation, line following, and basic junction response."""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

import map
import motors
import time


def line_correction(line_sensor_readings):
    """Apply one steering correction based on the two center sensors."""

    # Sensors 1 and 2 are the inner pair; 1 means that sensor sees the line.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    # Pivot toward the side whose inner sensor still detects the line.
    if inner_sensors == [0, 1]:
        motors.bot.turn("right", speed=40)
    elif inner_sensors == [1, 0]:
        motors.bot.turn("left", speed=40)
    elif inner_sensors == [0, 0]:
        # Neither inner sensor sees the line, so reverse to search for it.
        motors.bot.reverse(speed=50)

def line_following(line_sensor_readings, read_sensors):
    """Follow a line and classify junctions using a fresh-reading callback."""

    # The middle sensors track the path; the outer pair flags a junction.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]

    if outer_sensors != [0, 0]:
        # A second sample is required to distinguish junction patterns.

        # Let the classifier take a fresh sample after moving onto the junction.
        junction = map.node(line_sensor_readings).decide_node_type(read_sensors)
        print(junction)
        if junction is not None:
            # Navigation choices at junctions are not defined yet; keep the robot stopped.
            motors.bot.stop()
            time.sleep(1)
            if junction == "Right turn":
                motors.bot.forward()
                time.sleep(0.3)
                motors.bot.turn("right")
                time.sleep(1.8)
            elif junction == "Left turn":
                motors.bot.forward()
                time.sleep(0.3)
                motors.bot.turn("left")
                time.sleep(1.5)
            elif junction == "T junction":
                motors.bot.reverse()
                time.sleep(0.5)
                motors.bot.turn("right")
                time.sleep(7)
            elif junction == "Cross junction":
                pass
            elif junction == "Right T junction":
                pass
            elif junction == "Left T junction":
                pass

            return junction

    if inner_sensors == [1, 1]:
        # Both inner sensors see the line, so continue straight.
        motors.bot.forward(speed=60)
    else:
        # At least one inner sensor has lost the line; make one correction step.
        line_correction(line_sensor_readings)

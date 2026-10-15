"""Line-sensor validation, line following, and basic junction response."""

import map
import time
import motors


def line_correction(line_sensor_readings):
    """Apply one steering correction based on the two center sensors."""
    _validate_reading(line_sensor_readings)

    # Sensors 1 and 2 are the inner pair; 1 means that sensor sees the line.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    # Pivot toward the side whose inner sensor still detects the line.
    if inner_sensors == [0, 1]:
        motors.bot.turn("right", speed=60)
    elif inner_sensors == [1, 0]:
        motors.bot.turn("left", speed=60)
    elif inner_sensors == [0, 0]:
        # Neither inner sensor sees the line, so reverse to search for it.
        motors.bot.reverse(speed=30)


def _validate_reading(reading):
    """Require exactly four binary sensor states before controlling motors."""
    if len(reading) != 4 or any(value not in (0, 1) for value in reading):
        raise ValueError("A line-sensor reading must contain four binary values.")


def line_following(line_sensor_readings, read_sensors=None):
    """Follow a line and classify junctions using a fresh-reading callback."""
    _validate_reading(line_sensor_readings)

    # The middle sensors track the path; the outer pair flags a junction.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]

    if outer_sensors != [0, 0]:
        # A second sample is required to distinguish junction patterns.
        if read_sensors is None:
            motors.bot.stop()
            raise RuntimeError("Junction handling requires a fresh sensor-reading callback.")

        # Advance carefully, then stop to capture the second junction pattern.
        motors.bot.stop()
        motors.bot.forward(speed=30)
        time.sleep(0.5)
        motors.bot.stop()
        reading2 = read_sensors()
        _validate_reading(reading2)

        # Classify the original and fresh readings as one junction observation.
        junction = map.node(line_sensor_readings, reading2).decide_node_type()
        if junction == "T junction":
            # Navigation choices at junctions are not defined yet; keep the robot stopped.
            motors.bot.stop()
        elif junction == "Cross junction":
            motors.bot.stop()
        elif junction == "Right turn":
            motors.bot.turn("right", speed=60)
            motors.bot.forward()
        elif junction == "Left turn":
            motors.bot.turn("left", speed=60)
            motors.bot.forward()
        else:
            # Stop for unknown patterns and junction types without a route policy.
            motors.bot.stop()
        return junction

    elif inner_sensors == [1, 1]:
        # Both inner sensors see the line, so continue straight.
        motors.bot.forward(speed=60)
    else:
        # At least one inner sensor has lost the line; make one correction step.
        line_correction(line_sensor_readings)

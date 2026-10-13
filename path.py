import map
import time # tmporary for testing - Remove later before setting up a new time test for proper software


def line_correction(line_sensor_readings):
    """Choose a correction action based on the two inner sensor readings."""

    # The inner sensors indicate whether the robot is left, right, or off line.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    if inner_sensors == [0, 1]:
        # speed up left motor and slow down right motor to get back on the line
        pass
    elif inner_sensors == [1, 0]:
        # slow down left motor and speed up right motor to get back on the line
        pass
    elif inner_sensors == [0, 0]:
        # Stop both motors, then spin left and right to check which side
        # the line is on before correcting position.
        pass


def line_following(line_sensor_readings):
    """Classify sensor readings and print the corresponding driving status."""

    # The middle pair tracks the line; the outer pair detects junction patterns.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]

    if outer_sensors != [0, 0]:
        # robot is at a junction
        print("Junction detected")
        reading1 = line_sensor_readings
        # A second reading is intended to help classify the junction.
        reading2 = line_sensor_readings
        junction = map.node.decide_node_type(map.node, [reading1, reading2])
        print(f"Junction type: {junction}")

    elif inner_sensors == [1, 1]:
        # robot is on line with no junctions
        print("Moving forward")
    elif inner_sensors == [1, 0]:
        # robot has veered slightly to the right of the line
        on_line = False
        # Stop trying to correct after half a second, even if recovery fails.
        start_time = time.time()
        while not on_line and time.time() - start_time < 0.5:
            line_correction(line_sensor_readings)
            print("Slightly right")
            # Update line_sensor_readings here based on new sensor data
            on_line = inner_sensors == [1, 1]

    elif inner_sensors == [0, 1]:
        # robot has veered slightly to the left of the line
        on_line = False
        # Bound the correction attempt so it cannot loop indefinitely.
        start_time = time.time()
        while not on_line and time.time() - start_time < 0.5:
            line_correction(line_sensor_readings)
            print("Slightly left")
            # Update line_sensor_readings here based on new sensor data
            on_line = inner_sensors == [1, 1]

    elif inner_sensors == [0, 0]:
        # robot has veered off the line completely
        on_line = False
        # Bound the correction attempt so it cannot loop indefinitely.
        start_time = time.time()
        while not on_line and time.time() - start_time < 0.5:
            line_correction(line_sensor_readings)
            print("Off the line")
            # Update line_sensor_readings here based on new sensor data
            on_line = inner_sensors == [1, 1]

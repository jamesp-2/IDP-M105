import map
import time # temporary for testing - Remove later before setting up a new time test for proper software
from machine import Pin #type: ignore
import motors


def line_correction(line_sensor_readings):
    """Choose a correction action based on the two inner sensor readings."""

    # The inner sensors indicate whether the robot is left, right, or off line.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    if inner_sensors == [0, 1]:
        # speed up left motor and slow down right motor to get back on the line
        motors.Bot.turn("left", speed=60)
    elif inner_sensors == [1, 0]:
        # slow down left motor and speed up right motor to get back on the line
        motors.Bot.turn("right", speed=60)
    elif inner_sensors == [0, 0]:
        # reverse motors to back up and search for the line, since the robot is off the line completely
        # the line is on before correcting position.
        motors.Bot.reverse(speed=30)


def line_following(line_sensor_readings):
    """Classify sensor readings and print the corresponding driving status."""

    # The middle pair tracks the line; the outer pair detects junction patterns.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]

    if outer_sensors != [0, 0]:
        # robot is at a junction
        reading1 = line_sensor_readings
        # A second reading is intended to help classify the junction.
        motors.Bot.stop()  # Stop the robot to take a second reading for junction classification
        motors.Bot.forward(speed=30) # Move forward slightly to get a second reading
        time.wait(0.5)  # Wait for a short duration to allow the robot to move forward
        motors.Bot.stop()  # Stop the robot again to take the second reading
        reading2 = line_sensor_readings
        junction = map.node.decide_node_type(map.node, [reading1, reading2])
        if junction == "T junction":
            # Handle T junction logic here
            pass
        elif junction == "Cross junction":
            # Handle Cross junction logic here
            pass
        elif junction == "Right turn":
            # Handle Right turn logic here
            motors.Bot.turn("right", speed=60)
            motors.Bot.forward()  # Move forward after turning
        elif junction == "Left turn":
            # Handle Left turn logic here
            motors.Bot.turn("left", speed=60)
            motors.Bot.forward()  # Move forward after turning  
        elif junction == "Right T junction":
            # Handle Right T junction logic here
            pass
        elif junction == "Left T junction":
            # Handle Left T junction logic here
            pass

    elif inner_sensors == [1, 1]:
        # robot is on line with no junctions
        motors.Bot.forward(speed=60)  # Move forward at full speed
    elif inner_sensors == [1, 0]:
        # robot has veered slightly to the right of the line
        on_line = False
        # Stop trying to correct after half a second, even if recovery fails.
        #start_time = time.time()
        while not on_line: #and time.time() - start_time < 0.5:
            line_correction(line_sensor_readings)
            # Update line_sensor_readings here based on new sensor data
            on_line = inner_sensors == [1, 1]

    elif inner_sensors == [0, 1]:
        # robot has veered slightly to the left of the line
        on_line = False
        # Bound the correction attempt so it cannot loop indefinitely.
        #start_time = time.time()
        while not on_line: #and time.time() - start_time < 0.5:
            line_correction(line_sensor_readings)
            # Update line_sensor_readings here based on new sensor data
            on_line = inner_sensors == [1, 1]

    elif inner_sensors == [0, 0]:
        # robot has veered off the line completely
        on_line = False
        # Bound the correction attempt so it cannot loop indefinitely.
        #start_time = time.time()
        while not on_line: #and time.time() - start_time < 0.5:
            line_correction(line_sensor_readings)
            # Update line_sensor_readings here based on new sensor data
            on_line = inner_sensors == [1, 1]

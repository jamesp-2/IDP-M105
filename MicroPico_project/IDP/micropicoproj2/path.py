"""Line-sensor validation, line following, and basic junction response."""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from mapping import *
import time
from motors import *
from sensors import *


def line_correction(line_sensor_readings, direction = "F"):
    """Apply one steering correction based on the two center sensors."""

    # Sensors 1 and 2 are the inner pair; 1 means that sensor sees the line.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    # Pivot toward the side whose inner sensor still detects the line.
    if inner_sensors == [0, 1]:
        bot.turn("right", 60)
    elif inner_sensors == [1, 0]:
        bot.turn("left", 60)
    elif inner_sensors == [0, 0]:
        # Neither inner sensor sees the line, so reverse to search for it.
        if direction == "R":
            bot.forward(30)
        else:
            bot.reverse(30)




def line_following(line_sensor_readings, read_sensors):
    """Follow a line and classify junctions using a fresh-reading callback."""

    # The middle sensors track the path; the outer pair flags a junction.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]

    if outer_sensors != [0, 0]:
        # A second sample is required to distinguish junction patterns.

        # Let the classifier take a fresh sample after moving onto the junction.
        junction = node(line_sensor_readings).decide_node_type(read_sensors)
        print(junction)
        if junction is not None:
            # Navigation choices at junctions are not defined yet; keep the robot stopped.
            bot.stop()
            time.sleep(1)
            if junction == "Right turn":
                bot.forward()
                time.sleep(0.3)
                bot.turn("right")
                time.sleep(1.8)
            elif junction == "Left turn":
                bot.forward()
                time.sleep(0.3)
                bot.turn("left")
                time.sleep(1.5)
            elif junction == "T junction":
                bot.reverse()
                time.sleep(0.5)
                bot.turn("right")
                time.sleep(7)
            elif junction == "Cross junction":
                pass
            elif junction == "Right T junction":
                pass
            elif junction == "Left T junction":
                pass

    elif inner_sensors == [1, 1]:
        # Both inner sensors see the line, so continue straight.
        bot.forward(speed=60)
    else:
        # At least one inner sensor has lost the line; make one correction step.
        line_correction(line_sensor_readings)


#Compares current and next direction to turn bot
def turn_to_direction(current_direction, next_direction, reverse):

    #Turn right
    if (next_direction - current_direction) % 4 == 1:
        bot.turn("left" if reverse else "right", speed=60)

    #Turn left    
    elif (current_direction - next_direction) % 4 == 1:
        bot.turn("right" if reverse else "left", speed=60)

    elif (next_direction - current_direction) % 4 == 2:
        bot.turn("right", speed=60)
        bot.turn("right", speed=60)

    return next_direction



#Moves until the next junction is reached
def move_to_junction():
    global current_junction

    while True:
        line_sensor_readings = read_line_sensors()
        junction = line_following(line_sensor_readings, read_line_sensors)
        if junction is not None:
            current_junction = junction
            return junction


def get_path_from_start(chosen_location):
    return path_from_start[chosen_location]


def rack_path(chosen_location):
    intended_path = get_path_from_start(chosen_location)
    if intended_path[0] == "E":
        rack_location = first_available_slot(bottom_right_rack)
    elif intended_path[0] == "W":
        rack_location = first_available_slot(bottom_left_rack)
    return

def follow_path(chosen_location, current_direction, current_path):

    intended_path = get_path_from_start(chosen_location)


    #Backtracking
    while current_path != intended_path[:len(current_path)]:
        current_direction = turn_to_direction(current_direction, current_path[-1], True)
        move_to_junction()
        current_path.pop()

    #Following forward route
    while len(current_path) < len(intended_path):
        next_step = intended_path[len(current_path)]
        current_direction = turn_to_direction(current_direction, next_step, False)
        current_path.append(next_step)
        move_to_junction()

    bot.stop()
    return current_direction



#For extra points will return to start
def go_to_start(current_path, current_direction):
    return follow_path("START", current_direction, current_path)


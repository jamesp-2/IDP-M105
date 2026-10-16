"""Line-sensor validation, line following, and basic junction response."""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from mapping import *
import time
from motors import *


def line_correction(line_sensor_readings):
    """Apply one steering correction based on the two center sensors."""

    # Sensors 1 and 2 are the inner pair; 1 means that sensor sees the line.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    # Pivot toward the side whose inner sensor still detects the line.
    if inner_sensors == [0, 1]:
        bot.turn("right", speed=60)
    elif inner_sensors == [1, 0]:
        bot.turn("left", speed=60)
    elif inner_sensors == [0, 0]:
        # Neither inner sensor sees the line, so reverse to search for it.
        bot.reverse(speed=30)





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
        if read_sensors is None:
            bot.stop()
            raise RuntimeError("Junction handling requires a fresh sensor-reading callback.")

        # Advance carefully, then stop to capture the second junction pattern.
        bot.stop()
        bot.forward(speed=30)
        time.sleep(0.5)
        bot.stop()
        reading2 = read_sensors()

        # Classify the original and fresh readings as one junction observation.
        junction = node(line_sensor_readings, reading2).decide_node_type()
        if junction == "T junction":
            # Navigation choices at junctions are not defined yet; keep the robot stopped.
            bot.stop()
        elif junction == "Cross junction":
            bot.stop()
        elif junction == "Right turn":
            bot.turn("right", speed=60)
            bot.forward()
        elif junction == "Left turn":
            bot.turn("left", speed=60)
            bot.forward()
        else:
            # Stop for unknown patterns and junction types without a route policy.
            bot.stop()
        return junction


    if inner_sensors == [1, 1]:
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

    current_direction = next_direction
    return next_direction



#Moves until the next junction is reached
def move_to_junction():
    #Move until junction is reached
    #Move until detection by line_following function?
    pass


def get_path_from_start(chosen_location):
    return path_from_start[chosen_location]


def follow_path(chosen_location, current_direction, current_path):

    intended_path = get_path_from_start(chosen_location)

    #Bot is at start
    if len(current_path) == 0:
        #Turn to direction of first step
        current_direction = turn_to_direction(current_direction, intended_path[0], False)
        #Move until junction is reached
        #Add to current location
        current_path.append(intended_path[0])
    
    for i in range(len(current_path)):
        if current_path[i] != intended_path[i]:
            #Turn to opposite direction of current step
            current_direction = turn_to_direction(current_direction, intended_path[i], True)
            #Move until junction is reached
            #Remove last location
            pass
        else: 
            #Turn to direction of next step
            current_direction = turn_to_direction(current_direction, intended_path[i], False)
            #Move until junction is reached
            #Add to current location
            current_path.append(intended_path[i])




    
    



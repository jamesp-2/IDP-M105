"""Line-sensor validation, line following, and basic junction response."""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

from mapping import *
import time
from motors import *


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


#Compares current and next direction to turn bot
#def turn_to_direction(current_direction, next_direction, reverse):

    #Turn right
#    if (next_direction - current_direction) % 4 == 1:
#        bot.turn("left" if reverse else "right", speed=60)

    #Turn left    
#    elif (current_direction - next_direction) % 4 == 1:
#        bot.turn("right" if reverse else "left", speed=60)

#    elif (next_direction - current_direction) % 4 == 2:
#        bot.turn("right", speed=60)
#        bot.turn("right", speed=60)

#    current_direction = next_direction
#    return next_direction


#Moves until the next junction is reached
#def move_to_junction():
    #Move until junction is reached
    #Move until detection by line_following function?
#    pass


#def get_path_from_start(chosen_location):
#    return path_from_start[chosen_location]


#def follow_path(chosen_location, current_direction, current_path):

#    intended_path = get_path_from_start(chosen_location)

    #Bot is at start
#    if len(current_path) == 0:
        #Turn to direction of first step
#        current_direction = turn_to_direction(current_direction, intended_path[0], False)
        #Move until junction is reached
        #Add to current location
#        current_path.append(intended_path[0])
    
#    for i in range(len(current_path)):
#        if current_path[i] != intended_path[i]:
            #Turn to opposite direction of current step
#            current_direction = turn_to_direction(current_direction, intended_path[i], True)
            #Move until junction is reached
            #Remove last location
#            pass
#        else: 
            #Turn to direction of next step
#            current_direction = turn_to_direction(current_direction, intended_path[i], False)
            #Move until junction is reached
            #Add to current location
#            current_path.append(intended_path[i])

# Integrated Design Project M105

## Project Overview

This project includes the code used for the integrated design project. It includes files containing line following and route planning algorithms that respond to external readings.

## Features

* Use of multiple files in order to make the code more manageable rather than one big file with every function.
* Use of classes to make the controlling of special objects easier, such as the motors.
* Comments explaining each function to aid understanding of the code across contributors.
* Configuration file to hold information on pin layouts so everyone can easily use each sensor without needing to know where it is plugged in, as well as allowing quick global changes to pin selections
* Clearly named variables to make comprehension easier for those not writing the code

## Code Structure
**main.py:**

Holds main while loop for the robot to function during operation. Detects start button presses to start the main software.

##

**config.py:**

Contains the pin numbers for each sensor/ output connected to the pico. 

##

**sensors.py, claw.py, motors.py:**

Sets up classes and functions for the respective devices for easy operation in other files. 

*sensors.py* -- contains the functions for the IR sensor, HE sensor, distance sensor and line tracking sensors.

*claw.py* -- sets up the servo class, which is then used in the functions within this file in order to carry out the pickup/ delivery functions which can then be used in other files to easily close/ open and lift/ lower grabber.

*motors.py* -- defines a motor class, followed by the bot class which is used to control the movement of the robot through simple forward(), reverse(), turn() functions for easier implementation.

##

**pathing.py, line_correction.py, mapping.py:**

These files contain the main logic of the robot that it uses to move and complete the tasks.

*pathing.py* -- contains the bulk of the operation of the robot. Tells it what to do at different junctions on the map, gives instructions on how to pickup/ deliver the boxes, controls general movement around the map.

*line_correction.py* -- handles getting the robot back onto the line if it detects that it is no longer straight on the path.

*mapping.py* -- holds every route and the order of pickup locations to be followed. Defines the route class that is used to generate whole routes based on current task and sensor readings.
Takes sensor readings and decides what path should be followed, turns on the corresponding LED, as well as adjusting which slot in the rack to go to depending on which slots are available.
Also defines the rack class which is used to hold information about each rack and which slots are free.

##

**test files:**

Miscellaneous files containing tests for different sensors during development

## Algorithm Structure

<img width="530" height="1152" alt="image(1)" src="https://github.com/user-attachments/assets/956b1ab5-bcf6-44e7-af62-c2183ffaa8a9" />




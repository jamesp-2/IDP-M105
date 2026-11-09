# Integrated Design Project M105

## Project Overview

This project includes the code used for the integrated design project. It includes files containing line following and route planning algorithms that respond to external readings.

## System Diagram

<img width="653" height="451" alt="Screenshot 2026-11-08 at 17 30 08" src="https://github.com/user-attachments/assets/2fc57ef5-4288-4376-9f89-0e67295cd8b4" />


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

*leds.py* -- defines the led class for easy operation in the rest of the code.

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

## Classes and Key Functions

**Classes:**

*Servo* -- This class sets up the ability to control the servo motors by transforming the desired angle into a PWM duty value that can be passed to the servo. This is then used to create the close_claw(), open_claw(), lift(), lower(), etc. functions.

*Motor and Bot* -- The motor class allows the control of individual motors through input of a value from 0-100, this is translated to a PWM duty value which is then fed to the motor. The Bot class furthers this by defining functions that allow the powering of both motors at the same time, allowing the robot to be controlled through simple commands like forward(), reverse(), turn(direction).

*LED* -- Allows the control of all three LEDs by defining the red, yellow and green LEDs separately, also sets up the flash() function to make the yellow LED flash while the robot is operating.

*route* -- This class controls the entire route generation of the robot. The pickup location is passed into the class when a route object is created and from this the pickup route is determined through start_route(). The HE sensor is then used to create the delivery route in delivery_pathfinding(), which also sets the LEDs to the correct values. Once delivery has been completed it then is used to generate the return route.

*rack* -- Sets up racks, storing which slots have boxes in them, and allowing the robot to determine the first available slot using the defined function of the same name.

##

**Key Functions:**

*main()* -- loops until the start button is pressed, sets up state of robot and then calls pathing() to carry out the rest of the robots functions.

*line_correction()* -- Is only called when the middle two line tracking sensors do not read [1,1], i.e. the robot is not centred on the line. Very simple function, just causes the robot to turn in the opposite direction to the way it is off the line, function stops being called when readings are back to [1, 1].

*build_route(), pathing() and route_following()* -- pathing() uses the build_route() function to create a pickup path before calling the route_following() function. route_following() is used to detect junctions and follow the straight lines between them. It also controls the dead zone between junction detection to avoid double readings on the same corner. route_following() is also used to call the handle_junction() function.

*handle_junction()* -- This function essentially translates the route of the robot into what actions to perform when at a junction and increments the counter that detects when the route is complete.

directional functions called by handle_junction:

* *perform_straight_move()* -- Robot continue straight
* *perform_turn()* -- Turns a specified direction for a short time, then keeps turning until inner line sensors both read 1, followed by a short turn to centre the robot more.

*perform_task_move()* -- Handles both pickup and delivery operations. performs same turn with slightly different timings as perform_turn(), the robot then continues straight along the path until the line tracking sensors read the target state, defined by the task type. Then the grabber is controlled in order to complete the task specified. Finally, reverses out until it reaches the back line which defines the regular path.

*start_alignment()* -- turns the robot at the start of the run to be aligned with whichever direction it is going first.

sensor functions:
* *read_line_sensors()* -- gets line tracking readings and returns them as a list.
* *get_distance()* -- uses VL53L0X.py file to get data out of the distance sensor, then takes an average from 10 values and scales reading down to easier values to deal with.
* *get_magnetic_reading()* -- similar process to get_distance, but uses data to get a north or south reading.

## Algorithm Structure

<img width="530" height="1052" alt="image(1)" src="https://github.com/user-attachments/assets/14b85557-1aed-44c0-9c36-065d2edaa214" />







import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

import motors
import time
import mapping
import path
import sensors
import claw
import config
from leds import *

route_counter = 0
active_route = None
junction_handled = False
clear_sensor_samples = 0
CLEAR_SAMPLES_REQUIRED = 10
current_pickup_index = 0
led = LED()
led.start()


def read_line_sensors():
    """Return the current line sensor values from left to right."""
    return [sensor.value() for sensor in sensors.track_sensors]


def build_route(pickup_path):
    """Build the route plan for the selected pickup path."""
    route_plan = mapping.route(pickup_path)
    route_plan.start_route()
    return route_plan


def pathing(line_sensor_readings, pickup_route):
    """Follow the next instruction or correct the robot on the track."""
    global route_counter, active_route

    if active_route is None:
        active_route = build_route(pickup_route)

    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]
    route = active_route.sel_route

    if route_counter >= len(route):
        motors.bot.stop()
        return

    route_following(outer_sensors, inner_sensors, route, line_sensor_readings)


def route_following(outer_sensors, inner_sensors, route_plan, line_sensor_readings):
    """Handle a junction or keep the robot centred on the line."""
    global route_counter, junction_handled, clear_sensor_samples

    if outer_sensors == [0, 0]:
        clear_sensor_samples += 1
        if clear_sensor_samples >= CLEAR_SAMPLES_REQUIRED:
            junction_handled = False
    elif junction_handled:
        clear_sensor_samples = 0
        return
    else:
        clear_sensor_samples = 0

    if outer_sensors != [0, 0]:
        handle_junction(route_plan, line_sensor_readings)
    elif inner_sensors == [1, 1]:
        motors.bot.forward()
    else:
        path.line_correction(line_sensor_readings)


def handle_junction(route_plan, line_sensor_readings):
    """Execute the next movement for the current route instruction."""
    global route_counter, junction_handled, clear_sensor_samples, active_route, current_pickup_index

    junction_handled = True
    clear_sensor_samples = 0
    print("junction")

    motors.bot.stop()
    motors.bot.forward()
    time.sleep(0.43)

    action = route_plan[route_counter]

    if action == "straight":
        perform_straight_move()
    elif action == "left":
        perform_turn("left")
    elif action == "right":
        perform_turn("right")
    elif action == "reverse":
        perform_reverse_move(line_sensor_readings)
    elif action == "left into pickup":
        perform_task_move("left", "pickup", active_route)
    elif action == "right into pickup":
        perform_task_move("right", "pickup", active_route)
    elif action == "left into delivery":
        perform_task_move("left", "delivery", active_route)
    elif action == "right into delivery":
        perform_task_move("right", "delivery", active_route)

    route_counter += 1

    if route_counter < len(route_plan):
        print(route_plan[route_counter])
    else:
        motors.bot.stop()

        global active_route, current_pickup_index
        active_route = None
        route_counter = 0
        current_pickup_index += 1


def perform_straight_move():
    """Keep moving straight through a junction."""
    print("straight")
    motors.bot.forward()


def perform_turn(direction):
    """Turn until the centre sensors find the line again."""
    print(direction)
    motors.bot.turn(direction)
    time.sleep(1.5)
    motors.bot.stop()

    line_sensor_readings = read_line_sensors()
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    while inner_sensors != [1, 1]:
        motors.bot.turn(direction)
        line_sensor_readings = read_line_sensors()
        inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    path.line_correction(line_sensor_readings)


def perform_reverse_move(line_sensor_readings):
    """Reverse and pull the robot back onto the line."""
    print("reverse")
    path.line_correction(line_sensor_readings, "R")
    motors.bot.reverse()


def perform_task_move(direction, task_type, active_route):
    """Enter the task zone and wait until the target sensor pattern is reached."""
    global route_counter, junction_handled, clear_sensor_samples

    if task_type not in ("pickup", "delivery"):
        raise ValueError("task_type must be 'pickup' or 'delivery'")

    if task_type == "pickup":
        target_sensor_state = [1, 1, 1, 1]
    else:
        target_sensor_state = [0, 0, 0, 0]
    print(task_type)

    motors.bot.turn(direction)
    time.sleep(1.4)

    line_sensor_readings = read_line_sensors()
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    while inner_sensors != [1, 1]:
        motors.bot.turn(direction)
        line_sensor_readings = read_line_sensors()
        inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    motors.bot.turn(direction)
    time.sleep(0.2)

    while line_sensor_readings != target_sensor_state:
        inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
        if inner_sensors == [1, 1]:
            motors.bot.forward()
        else:
            path.line_correction(line_sensor_readings)
        time.sleep_ms(25)
        line_sensor_readings = read_line_sensors()

    motors.bot.stop()
    if task_type == "pickup":
        claw.lower()
        time.sleep(0.7)
        claw.close_claw()
        time.sleep(1)
        claw.lift()
        time.sleep(1)

        active_route.delivery_pathfinding()
        
    else:
        claw.lower_small()
        claw.open_claw_small()
        led.red.value(Off)
        led.yellow.value(Off)
        led.green.value(Off)

        active_route.return_pathfinding()
        active_route.target_rack.slot_is_full(active_route.target_slot)

    line_sensor_readings = read_line_sensors()
    task_zone_cleared = False
    while True:
        outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]
        if outer_sensors == [0, 0]:
            task_zone_cleared = True
        elif task_zone_cleared:
            break

        inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
        if inner_sensors == [1, 1] or inner_sensors == [0, 0]:
            motors.bot.reverse()
        else:
            path.line_correction(line_sensor_readings, "R")

        time.sleep_ms(25)
        line_sensor_readings = read_line_sensors()

    motors.bot.stop()

    #if slot_state == 1:
        #if direction == "left":
            #perform_turn("right")
        #else:
            #perform_turn("left")

    junction_handled = False
    clear_sensor_samples = CLEAR_SAMPLES_REQUIRED
    if task_type == "delivery":
        claw.lift()
        claw.open_claw()


def start_alignment(direction):
    """Rotate until the centre sensors find the line and stop."""
    motors.bot.turn(direction)
    time.sleep(0.5)

    line_sensor_readings = read_line_sensors()
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    while inner_sensors != [1, 1]:
        print([line_sensor_readings[0], line_sensor_readings[1], line_sensor_readings[2], line_sensor_readings[3]])
        motors.bot.turn(direction)
        line_sensor_readings = read_line_sensors()
        inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    motors.bot.turn(direction)
    time.sleep(0.2)
    motors.bot.stop()

time.sleep(2)
if config.button.value() == 1:

    start_alignment("left")
    claw.lift()
    claw.open_claw()

    while True:
        led.flash()
        if current_pickup_index >= len(mapping.task_list):
            motors.bot.stop()
            break

        readings = read_line_sensors()
        print(readings)

        current_task_name = mapping.task_list[current_pickup_index]
        current_pickup_path = mapping.paths.get(current_task_name)
        print(current_pickup_path)
        pathing(readings, current_pickup_path)
        time.sleep_ms(25)



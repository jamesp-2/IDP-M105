"""Monday line-following test routine.

This script follows a fixed route using the line sensors and motor control
utilities.
"""

import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

import motors
import time
import mapping
import path
import sensors

# Route state used to track where the robot is in the test sequence.
# route_counter indexes the next action in the route list, while the other flags
# stop repeated turn handling when the robot is briefly in a clear section.
route_counter = 0
junction_handled = False
clear_sensor_samples = 0
CLEAR_SAMPLES_REQUIRED = 10


def read_line_sensors():
    """Return the current digital states in left-to-right sensor order."""
    return [sensor.value() for sensor in sensors.track_sensors]


def build_monday_route():
    """Create the route pattern for the Monday test, including rack-based spacing."""
    monday_test_route = [
        "straight",
        "left",
        "left into pickup",
        "right",
    ]

    for _ in range(mapping.bottom_right_rack.first_available_slot()):
        monday_test_route.append("straight")

    monday_test_route.extend([
        "left into delivery",
        "right",
        "right",
        "straight",
    ])
    return monday_test_route


def test_path(line_sensor_readings):
    """Check the current sensor state and follow the next route instruction."""
    global route_counter

    # These sensor pairs are used for different checks:
    # - inner sensors: the centre line detection
    # - outer sensors: junction detection on either side of the line
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]

    # The route is recreated each scan so the sequence is based on the current
    # rack state, but the movement progress itself is still tracked by
    # route_counter.
    monday_test_route = build_monday_route()

    if route_counter >= len(monday_test_route):
        motors.bot.stop()
        return

    route_following(outer_sensors, inner_sensors, monday_test_route, line_sensor_readings)


def route_following(outer_sensors, inner_sensors, monday_test_route, line_sensor_readings):
    """Handle either a junction or a normal line-correction update."""
    global route_counter, junction_handled, clear_sensor_samples

    # If both outer sensors are off, the robot is likely in a clear stretch.
    # Keep a few samples before allowing another junction to be processed.
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
        handle_junction(monday_test_route, line_sensor_readings)
    elif inner_sensors == [1, 1]:
        motors.bot.forward()
    else:
        path.line_correction(line_sensor_readings)


def handle_junction(monday_test_route, line_sensor_readings):
    """Execute the next movement for the current junction instruction."""
    global route_counter, junction_handled, clear_sensor_samples

    junction_handled = True
    clear_sensor_samples = 0
    print("junction")

    # Stop briefly before turning so the route action can be executed exactly.
    motors.bot.stop()
    motors.bot.forward()
    time.sleep(0.3)

    # Each junction uses the current route instruction for this step. Once the
    # motion finishes, route_counter advances so the next junction uses the next
    # instruction in the list.
    action = monday_test_route[route_counter]

    if action == "straight":
        perform_straight_move(line_sensor_readings)
    elif action == "left":
        perform_turn("left")
    elif action == "right":
        perform_turn("right")
    elif action == "reverse":
        perform_reverse_move(line_sensor_readings)
    elif action == "left into pickup":
        perform_task_move("left", "pickup")
    elif action == "right into pickup":
        perform_task_move("right", "pickup")
    elif action == "left into delivery":
        perform_task_move("left", "delivery")
    elif action == "right into delivery":
        perform_task_move("right", "delivery")

    route_counter += 1

    if route_counter < len(monday_test_route):
        print(monday_test_route[route_counter])
    else:
        motors.bot.stop()


def perform_straight_move(line_sensor_readings):
    """Continue straight while centring on the line."""
    print("straight")
    motors.bot.forward()
    path.line_correction(line_sensor_readings)


def perform_turn(direction):
    """Turn in the given direction until the centre sensors detect the line again."""
    print(direction)
    motors.bot.turn(direction)
    time.sleep(0.8)
    motors.bot.stop()

    line_sensor_readings = read_line_sensors()
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    while inner_sensors != [1, 1]:
        motors.bot.turn(direction)
        line_sensor_readings = read_line_sensors()
        inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    path.line_correction(line_sensor_readings)


def perform_reverse_move(line_sensor_readings):
    """Reverse and then re-centre on the line."""
    print("reverse")
    path.line_correction(line_sensor_readings, "R")
    motors.bot.reverse()


def perform_task_move(direction, task_type):
    """Turn into a task zone and hold until the required sensor target is reached."""
    task_type = task_type.lower()
    if task_type not in ("pickup", "delivery"):
        raise ValueError("task_type must be 'pickup' or 'delivery'")

    target_sensor_state = [1, 1, 1, 1] if task_type == "pickup" else [0, 0, 0, 0]
    print(task_type)

    motors.bot.turn(direction)
    time.sleep(0.8)

    line_sensor_readings = read_line_sensors()
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    while inner_sensors != [1, 1]:
        motors.bot.turn(direction)
        line_sensor_readings = read_line_sensors()
        inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    motors.bot.turn(direction)
    time.sleep(0.1)

    # Continue until the target sensor state is reached. Pickup uses all sensors
    # active, while delivery waits for the robot to reach the clear sensor state.
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
        # Box pickup goes here.
        pass
    else:
        # Box delivery goes here.
        pass

    # Reverse-follow the line until the robot has cleared the task zone and
    # reaches the outer sensors at the main-track junction.
    line_sensor_readings = read_line_sensors()
    task_zone_cleared = False
    while True:
        outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]
        if outer_sensors == [0, 0]:
            task_zone_cleared = True
        elif task_zone_cleared:
            break

        inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
        if inner_sensors == [1, 1]:
            motors.bot.reverse()
        else:
            path.line_correction(line_sensor_readings, "R")

        time.sleep_ms(25)
        line_sensor_readings = read_line_sensors()

    # Stop at the main-track junction so normal route following can continue.
    motors.bot.stop()

    # Pull in the global state variables
    global junction_handled, clear_sensor_samples
    
    # Manually reset the flags so the software knows the previous turn is finished
    # and it is allowed to read the tape it is currently sitting on.
    junction_handled = False
    clear_sensor_samples = CLEAR_SAMPLES_REQUIRED


def start_alignment(direction):
    """Rotate the robot until the centre sensors detect the line and stop."""
    motors.bot.turn(direction)
    time.sleep(0.5)

    line_sensor_readings = read_line_sensors()
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    while inner_sensors != [1, 1]:
        motors.bot.turn(direction)
        line_sensor_readings = read_line_sensors()
        inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]

    motors.bot.turn(direction)
    time.sleep(0.1)
    motors.bot.stop()


# Start the robot aligned with the line before entering the main test loop.
# This calibration step keeps the robot centred on the line before it starts the
# route-based movement sequence.
start_alignment("right")

# Main control loop for the line-following test.
# Each pass samples the sensors and executes the next route instruction if a
# junction or correction is needed.
while True:
    readings = read_line_sensors()
    print(readings)
    test_path(readings)
    time.sleep_ms(25)

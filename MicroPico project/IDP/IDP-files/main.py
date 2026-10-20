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

# ---------------------------------------------------------------------------
# The robot uses a simple state machine for the Monday route test.
#
# The route is stored as a list of instructions such as "left", "straight", or
# "left into pickup". Each time the robot reaches a junction, the next entry in
# the list is executed. The state variables below track progress and guard
# against repeat-triggering while the robot passes over clear tape sections.
# ---------------------------------------------------------------------------
route_counter = 0
junction_handled = False
clear_sensor_samples = 0
CLEAR_SAMPLES_REQUIRED = 10


def read_line_sensors():
    """Return the current digital states in left-to-right sensor order."""
    # Each sensor is read using its own value() method. The returned list is
    # ordered from left-most to right-most sensor so the rest of the code can
    # reason about the line position consistently.
    return [sensor.value() for sensor in sensors.track_sensors]


def build_monday_route():
    """Create the route pattern for the Monday test, including rack-based spacing."""
    # The route is a sequence of movement instructions. The early part of the
    # route moves through the pickup branch and then extends straight through the
    # rack area for as many slots as are currently available.
    monday_test_route = [
        "straight",
        "left",
        "left into pickup",
        "right",
        "straight",
    ]

    # Add the route length needed for the current rack configuration. This keeps
    # the path aligned to the number of open slots before the delivery branch.
    for _ in range(mapping.bottom_right_rack.first_available_slot()):
        monday_test_route.append("straight")

    # Finish the route with the delivery section and return to the main track.
    monday_test_route.extend([
        "left into delivery",
        "left",
        "straight",
        "straight",
        "right",
        "straight",
    ])
    return monday_test_route


def test_path(line_sensor_readings):
    """Check the current sensor state and follow the next route instruction."""
    global route_counter

    # The robot needs to differentiate between a centre-line correction and a
    # junction. The inner sensors sit on the line itself, while the outer sensors
    # tell us when the robot has reached the edge of a tape segment or a wider
    # junction area.
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]

    # Rebuild the route each time so the path reflects the current rack state,
    # while keeping the progress counter separate from the route itself.
    monday_test_route = build_monday_route()

    # Once the route is complete, stop the robot and leave the loop to finish.
    if route_counter >= len(monday_test_route):
        motors.bot.stop()
        return

    route_following(outer_sensors, inner_sensors, monday_test_route, line_sensor_readings)


def route_following(outer_sensors, inner_sensors, monday_test_route, line_sensor_readings):
    """Handle either a junction or a normal line-correction update."""
    global route_counter, junction_handled, clear_sensor_samples

    # If both outer sensors are off, the robot is likely in a clear section of
    # tape with no junction. Wait for several samples to confirm the robot has
    # truly left the junction area before re-enabling junction handling.
    if outer_sensors == [0, 0]:
        clear_sensor_samples += 1
        if clear_sensor_samples >= CLEAR_SAMPLES_REQUIRED:
            junction_handled = False
    elif junction_handled:
        # A junction was already handled, so do not trigger it again while the
        # robot remains in the same portion of the track.
        clear_sensor_samples = 0
        return
    else:
        clear_sensor_samples = 0

    # If there is a junction, execute the next route instruction; otherwise keep
    # the robot centred on the line.
    if outer_sensors != [0, 0]:
        handle_junction(monday_test_route, line_sensor_readings)
    elif inner_sensors == [1, 1]:
        motors.bot.forward()
    else:
        path.line_correction(line_sensor_readings)


def handle_junction(monday_test_route, line_sensor_readings):
    """Execute the next movement for the current junction instruction."""
    global route_counter, junction_handled, clear_sensor_samples

    # Once a junction is triggered, suppress repeat handling until the robot is
    # back on a clear section of the track.
    junction_handled = True
    clear_sensor_samples = 0
    print("junction")

    # Stop briefly before turning so the next movement is precise and does not
    # start while the robot is still drifting from the last line-correction.
    motors.bot.stop()
    motors.bot.forward()
    time.sleep(0.4)

    # Read the current route step and perform the matching movement. After the
    # action completes, advance the route counter so the next junction uses the
    # next instruction.
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

    # Print the next route step for debugging. When the final instruction has been
    # reached, stop the robot and exit the script cleanly.
    if route_counter < len(monday_test_route):
        print(monday_test_route[route_counter])
    else:
        motors.bot.forward()
        time.sleep(0.7)
        motors.bot.stop()
        time.sleep(1)
        sys.exit()


def perform_straight_move(line_sensor_readings):
    """Continue straight while centring on the line."""
    print("straight")
    # Continue driving forward while allowing the line-correction logic to keep
    # the robot centred on the tape.
    motors.bot.forward()
    path.line_correction(line_sensor_readings)


def perform_turn(direction):
    """Turn in the given direction until the centre sensors detect the line again."""
    print(direction)
    # Start the turn, wait a moment for the robot to commit to the arc, then
    # stop and continue rotating until the centre sensors are aligned again.
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
    # Reverse-drive while using the line-correction logic in reverse mode to pull
    # the robot back onto the centre of the line.
    path.line_correction(line_sensor_readings, "R")
    motors.bot.reverse()


def perform_task_move(direction, task_type):
    """Turn into a task zone and hold until the required sensor target is reached."""
    task_type = task_type.lower()
    if task_type not in ("pickup", "delivery"):
        raise ValueError("task_type must be 'pickup' or 'delivery'")

    # A pickup task is reached when all sensors see the line. A delivery task is
    # reached only once the robot is in the clear section beyond the task area.
    target_sensor_state = [1, 1, 1, 1] if task_type == "pickup" else [0, 0, 0, 0]
    print(task_type)

    # Turn into the target task area and continue until the robot is centred on
    # the line again before seeking the target sensor state.
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
        if inner_sensors == [1, 1] or inner_sensors == [0, 0]: "CHECK THIS STILL WORKS"
            motors.bot.reverse()
        else:
            path.line_correction(line_sensor_readings, "R")

        time.sleep_ms(25)
        line_sensor_readings = read_line_sensors()

    # Stop at the main-track junction so normal route following can continue.
    motors.bot.stop()

    # Pull in the global state variables so the robot can resume normal line
    # following after leaving the task area.
    global junction_handled, clear_sensor_samples

    # Manually reset the flags so the software knows the previous turn is
    # finished and it is allowed to read the tape it is currently sitting on.
    junction_handled = False
    clear_sensor_samples = CLEAR_SAMPLES_REQUIRED


def start_alignment(direction):
    """Rotate the robot until the centre sensors detect the line and stop."""
    # Use a short turn to bring the robot onto the line before the official route
    # starts. Once the centre sensors both see the line, stop the rotation and
    # leave the robot in a known starting pose.
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


# Give the robot a brief pause before calibration so the hardware has time to
# settle after power-up.
time.sleep(3)
# Start the robot aligned with the line before entering the main test loop.
# This calibration step keeps the robot centred before it begins following the
# route-based movement sequence.
start_alignment("right")

# Main control loop for the line-following test.
# Each pass samples the sensors and executes the next route instruction or line
# correction as needed.
while True:
    readings = read_line_sensors()
    print(readings)
    test_path(readings)
    time.sleep_ms(25)

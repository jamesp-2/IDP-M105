import sys

if "IDP-files" not in sys.path:
    sys.path.append("IDP-files")

import motors, time, mapping, path, sensors

route_counter = 0
junction_handled = False
clear_sensor_samples = 0
CLEAR_SAMPLES_REQUIRED = 10

def read_line_sensors():
    """Return the current digital states in left-to-right sensor order."""
    return [sensor.value() for sensor in sensors.track_sensors]

def test_path(line_sensor_readings):
    global route_counter

    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
    outer_sensors = [line_sensor_readings[0], line_sensor_readings[3]]

    monday_test_route = [ 
        "straight",
        "left", 
        "left into pickup",  
        "right",
    ]
    for _ in range(mapping.bottom_right_rack.first_available_slot()):
        monday_test_route.append("straight")
    monday_test_route.extend([
        "left", 
        "right", 
        "right", 
        "right", 
        "straight"
    ])

    if route_counter >= len(monday_test_route):
        motors.bot.stop()
        return

    route_following(outer_sensors, inner_sensors, monday_test_route, line_sensor_readings)

def route_following(outer_sensors, inner_sensors, monday_test_route, line_sensor_readings):
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
        junction_handled = True
        clear_sensor_samples = 0
        print("junction")
        motors.bot.stop()
        motors.bot.forward()
        time.sleep(0.3)
        if monday_test_route[route_counter] == "straight":
            print("straight")
            motors.bot.forward()
            path.line_correction(line_sensor_readings)
            route_counter += 1
        elif monday_test_route[route_counter] == "right":
            print("right")
            motors.bot.turn("right")
            time.sleep(0.8)
            motors.bot.stop()
            line_sensor_readings = read_line_sensors()
            inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
            while inner_sensors != [1, 1]:
                motors.bot.turn("right", 20)
                time.sleep(0.5)
                line_sensor_readings = read_line_sensors()
                inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
            path.line_correction(line_sensor_readings)
            route_counter += 1
        elif monday_test_route[route_counter] == "left":
            print("left")
            motors.bot.turn("left")
            time.sleep(0.8)
            motors.bot.stop()
            line_sensor_readings = read_line_sensors()
            inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
            while inner_sensors != [1, 1]:
                motors.bot.turn("left", 20)
                line_sensor_readings = read_line_sensors()
                inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
            path.line_correction(line_sensor_readings)
            route_counter += 1
        elif monday_test_route[route_counter] == "reverse":
            print("reverse")
            path.line_correction(line_sensor_readings)
            motors.bot.reverse(20)
            route_counter += 1
        elif monday_test_route[route_counter] == "left into pickup":
            motors.bot.turn("left")
            time.sleep(0.8)
            line_sensor_readings = read_line_sensors()
            inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
            while inner_sensors != [1, 1]:
                motors.bot.turn("left", 20)
                line_sensor_readings = read_line_sensors()
                inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
            while line_sensor_readings != [1, 1, 1, 1]:
                inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
                if inner_sensors == [1, 1]:
                    motors.bot.forward()
                else:
                    path.line_correction(line_sensor_readings)
                time.sleep_ms(25)
                line_sensor_readings = read_line_sensors()
            motors.bot.stop()
            # box pickup goes here
            motors.bot.reverse(10)
            route_counter += 1
        if route_counter < len(monday_test_route):
            print(monday_test_route[route_counter])
        else:
            motors.bot.stop()
    elif inner_sensors == [1, 1]:
        motors.bot.forward()
    else:
        path.line_correction(line_sensor_readings)

motors.bot.turn("right")
time.sleep(0.5)
line_sensor_readings = read_line_sensors()
inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
while inner_sensors != [1, 1]:
    motors.bot.turn("right")
    line_sensor_readings = read_line_sensors()
    inner_sensors = [line_sensor_readings[1], line_sensor_readings[2]]
motors.bot.turn("right")
time.sleep(0.1)
motors.bot.stop()

while True:
    readings = read_line_sensors()
    print(readings)
    test_path(readings)
    time.sleep_ms(25)

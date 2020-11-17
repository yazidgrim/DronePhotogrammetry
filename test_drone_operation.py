from djitellopy import Tello
import time

print("Create Tello Instance")

tello = Tello()

print("Connect to Tello Drone")
tello.connect()


print("Test 1 - Take off - Rotate - Land")
tello.takeoff()
tello.rotate_clockwise(360)
tello.land()

print("Test 2 - Take off - forward - back - left - right - Land")
tello.takeoff()
tello.move_forward(30)
tello.move_back(30)
tello.move_left(30)
tello.move_right(30)
tello.land()

print("Test 3 - Take off - Ascend - Descend - Land")
tello.takeoff()
tello.move_up(50)
tello.move_down(50)
tello.land()

print("Test 4 - Telemetry")
tello.takeoff()
tello.get_battery()
tello.get_current_state()
tello.get_height()
tello.get_pitch()
tello.get_roll()
tello.get_yaw()
tello.land







import time, cv2
from threading import Thread
from djitellopy import Tello

tello = Tello()

tello.connect()
time.sleep(1)
keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def videoRecorder():
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1/30)
    
    video.release()

recorder = Thread(target=videoRecorder)
recorder.start()
tello.get_battery()
tello.takeoff()
time.sleep(100)
tello.move_up(100)
tello.rotate_clockwise(360)
tello.land()
keepRecording = False
recorder.join()
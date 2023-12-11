import test_module as tm

from threading import Thread
from collections import deque

if __name__ == "__main__":
    try:
        # deque
        robot_control = deque()
        mid_point = deque()

        # subthreads
        thread_robot = Thread(target=tm.robotControl, args=(robot_control, ), daemon=True)
        thread_face = Thread(target=tm.faceDetect, args=(mid_point, ), daemon=True)

        # subthreads start
        thread_robot.start()
        thread_face.start()

        # main thread start
        print(f'main start')
        while True:
            if mid_point:
                point = mid_point.popleft()

                if len(point) > 1:

                    if (point[0]/2 - 100) < point[1][0] < (point[0]/2 + 100):
                        robot_control.append('f')

                    elif point[1][0] > (point[0]/2 + 100):
                        robot_control.append('r')

                    elif point[1][0] < (point[0]/2 - 100):
                        robot_control.append('l')

                else:
                    robot_control.append('s')
        
            else:
                continue

    except KeyboardInterrupt:
        pass
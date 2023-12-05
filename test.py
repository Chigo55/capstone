from robot import robotControl
from faceDetect import Detect


from threading import Thread
from collections import deque

if __name__ == "__main__":
    try:
        robot_control = deque()
        mid_point = deque()

        # STT 서브 스레드 생성
        thread_robot = Thread(target=robotControl, args=(robot_control, ), daemon=True)
        thread_face = Thread(target=Detect, args=(mid_point, ), daemon=True)

        # STT 서브 스레드 시작
        thread_robot.start()
        thread_face.start()

        # 메인 스레드 시작
        print(f'main start')
        while True:
            if mid_point:
                point = mid_point.popleft()

                if len(point) > 1:

                    if (point[0]/2 - 100) < point[1][0] < (point[0]/2 + 100):
                        robot_control.append('f')

                    elif point[1][0] > (point[0]/2 + 100):
                        robot_control.append('l')

                    elif point[1][0] < (point[0]/2 - 100):
                        robot_control.append('r')

                else:
                    robot_control.append('s')
        
            else:
                continue

    except KeyboardInterrupt:
        pass
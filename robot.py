import serial
import time

def robotControl(deque):
    try:
        py_serial = serial.Serial(port='COM3', baudrate=9600,)

        print(f'robot start')
        while True:
            if deque:
                commend = deque.popleft()
                print(commend)

                py_serial.write(commend.encode())

                if py_serial.readable():

                    # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
                    # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
                    response = py_serial.readline()

                    # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
                    print(response[:len(response)-1].decode())

            else:
                continue

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    robotControl()
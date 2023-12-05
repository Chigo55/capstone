import serial

# python - arduino serial 통신 함수
def robotControl(deque):
    py_serial = serial.Serial(port='COM3', baudrate=9600,)

    print(f'Control Start')
    while True:
        if deque:
            commend = deque.popleft()
            py_serial.write(commend.encode())

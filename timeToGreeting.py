import time
from playsound import playsound

# 시간대별 인사 함수
def timeToGreeting():
    times = time.localtime().tm_hour

    if times >= 5 and times <= 9:
        # 아침인사
        playsound("./audio/morning.mp3")

    elif times >= 12 and times <= 13:
        # 점심 인사
        playsound("./audio/lunch.mp3")

    elif times >= 19:
        # 저녁 인사
        playsound("./audio/dinner.mp3")

    else:
        playsound("./audio/hello.mp3")
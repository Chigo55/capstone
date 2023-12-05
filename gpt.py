import time
import os

from module import cherrybot
from robot import robotControl
from faceDetect import Detect
from playsound import playsound

from threading import Thread
from collections import deque

if __name__ == "__main__":
    try:
        api_key = 
        audio_path = 
        model = 

        speechs = deque()
        robot_control = deque()
        mid_point = deque()

        gpt = cherrybot(api_key, audio_path, model)

        # STT 서브 스레드 생성
        thread_stt = Thread(target=gpt.speechToText, args=(speechs, ), daemon=True)
        thread_robot = Thread(target=robotControl, args=(robot_control, ), daemon=True)
        thread_face = Thread(target=Detect, args=(mid_point, ), daemon=True)

        # STT 서브 스레드 시작
        thread_stt.start()

        is_speech = True
        is_greeting = False
        is_text = False
        is_answer = False
        is_play = False

        # 메인 스레드 시작
        while True:
            if mid_point:
                print(mid_point)
                point = mid_point.popleft()

                if point[1][0] < (point[0] + 20) or point[1][0] > (point[0] - 20):
                    robot_control.append('f')

                elif point[1][0] > (point[0] + 20):
                    robot_control.append('l')

                elif point[1][0] < (point[0] - 20):
                    robot_control.append('r')
                else:
                    robot_control.append('s')
                

            # # 스피치가 존재함
            # if speechs:

            #     # 스피치 감지 플레그 True
            #     if is_speech:
            #         speech = speechs.popleft()

            #         # 대화 시작 명령어 감지
            #         if speech.strip() == "안녕 체리":
            #             print("is_speech")
            #             is_speech = False
            #             is_greeting = True

            #     else:
            #         speech = speechs.popleft()

            #         # 대화 종료 명령어 감지
            #         if speech.strip() == "잘가 체리":
            #             is_speech = True
            #             is_greeting = False
            #             is_text = False
            #             is_answer = False
            #             is_play = False

            #         else:
            #             # 인사 플레그 True
            #             if is_greeting:
            #                 print("is_greeting")
            #                 times = time.localtime().tm_hour
            #                 gpt.timeToGreeting(times, is_greeting)
            #                 is_text = True
            #             else:
            #                 times = time.localtime().tm_hour
            #                 gpt.timeToGreeting(times, is_greeting)

            #             # 대화 입력 플레그 True
            #             if is_text:
            #                 print("is_text")
            #                 gpt_answer = gpt.chatGPT(speech)
            #                 is_answer = True

            #             # 답변 생성 플레그 True
            #             if is_answer:
            #                 print("is_answer")
            #                 gpt.textToSpeech(gpt_answer)
            #                 playsound(audio_path + "output.mp3")
            #                 is_play = True

            #             # 재생 플레그 True
            #             if is_play:
            #                 print("is_play")
            #                 os.remove(audio_path + "output.mp3")
            #                 is_greeting = False
            #                 is_text = False
            #                 is_answer = False
            #                 is_play = False
    except KeyboardInterrupt:
        pass

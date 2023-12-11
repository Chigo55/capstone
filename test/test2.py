import os
import test_module as tm
import time

from threading import Thread
from collections import deque
from playsound import playsound

if __name__ == "__main__":
    try:
        # api key, model 
        api_key = ""
        model = "gpt-4"

        # deque
        speechs = deque()
        texts = deque()

        # subthreads
        thrd_stt = Thread(target=tm.speech2Text, args=(speechs, ), daemon=True)

        # subthreads start
        thrd_stt.start()

        # flags
        is_speech = True
        is_greeting = False
        is_text = False
        is_answer = False
        is_play = False

        # main thread start
        while True:
            # 스피치가 존재함
            if speechs:

                # 스피치 감지 플레그 True
                if is_speech:
                    speech = speechs.popleft()

                    # 대화 시작 명령어 감지
                    if speech.strip() == "안녕":
                        print("is_speech")
                        is_speech = False
                        is_greeting = True

                else:
                    # 대화 종료 명령어 감지
                    speech = speechs.popleft()

                    if speech.strip() == "잘가":
                        print(f'is_bye')
                        is_speech = True
                        is_greeting = False
                        is_text = False
                        is_answer = False
                        is_play = False

                    # 대화 입력 플레그 True
                    if is_text:
                        print("is_text")
                        tm.chatGPT(api_key, model, speech, texts)
                        is_text = False
                        is_answer = True

                    # 답변 생성 플레그 True
                    if is_answer:
                        print("is_answer")
                        tm.text2Speech(api_key, texts)
                        is_answer = False
                        is_play = True

                    # 재생 플레그 True
                    if is_play:
                        print("is_play")
                        playsound("./audio/output.mp3")
                        os.remove("./audio/output.mp3")
                        is_play = False
                        is_text = True
                    
            # 인사 플레그 True
            if is_greeting:
                print("is_greeting")
                tm.time2Greeting()
                is_greeting = False
                is_text = True

    except KeyboardInterrupt:
        pass
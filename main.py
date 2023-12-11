
import os
import module as m

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
        robot_control = deque()
        mid_point = deque()

        # subthreads
        thrd_stt = Thread(target=m.speechToText, args=(speechs, ), daemon=True)
        thrd_robot = Thread(target=m.robotControl, args=(robot_control, ), daemon=True)
        thrd_detect = Thread(target=m.faceDetect, args=(mid_point, ), daemon=True)

        # subthreads start
        thrd_stt.start()
        thrd_robot.start()
        thrd_detect.start()

        # flags
        is_speech = True
        is_greeting = False
        is_text = False
        is_answer = False
        is_play = False

        # main thread start
        print(f'main start')
        while True:
                
            # recogntion speech
            if speechs:

                # speech flag True
                if is_speech:
                    speech = speechs.popleft()

                    # talk start command
                    if speech.strip() == "안녕":
                        is_speech = False
                        is_greeting = True

                else:
                    # talk end command
                    speech = speechs.popleft()
                    robot_control.append('s')

                    if speech.strip() == "잘가":
                        is_speech = True
                        is_greeting = False
                        is_text = False
                        is_answer = False
                        is_play = False

                    # text flag True
                    if is_text:
                        m.chatGPT(api_key, model, speech, texts)
                        robot_control.append('s')
                        is_text = False
                        is_answer = True

                    # answer flag True
                    if is_answer:
                        m.textToSpeech(api_key, texts)
                        robot_control.append('s')
                        is_answer = False
                        is_play = True

                    # play falg True
                    if is_play:
                        playsound("./audio/output.mp3")
                        os.remove("./audio/output.mp3")
                        robot_control.append('s')
                        is_play = False
                        is_text = True
                    
            # greeting flag True
            if is_greeting:
                m.timeToGreeting()
                is_greeting = False
                is_text = True
            
            # detect face
            if mid_point:
                point = mid_point.popleft()

                # face center point is exist
                if len(point) > 1:

                    # center
                    if (point[0]/2 - 100) < point[1][0] < (point[0]/2 + 100):
                        robot_control.append('f')

                    # left
                    elif point[1][0] > (point[0]/2 + 100):
                        robot_control.append('r')

                    # right
                    elif point[1][0] < (point[0]/2 - 100):
                        robot_control.append('l')

                # face center point is not exist
                else:
                    robot_control.append('s')
        
            else:
                continue

    except KeyboardInterrupt:
        pass

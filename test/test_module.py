import openai
import speech_recognition as sr
import cv2
import mediapipe as mp
import time
import serial
import os

from playsound import playsound


# 시간대별 인사 함수
def time2Greeting():
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


# Speech To Text 함수
def speech2Text(deque):
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print(f'STT Start')
            speech = r.listen(source)

        try:
            audio = r.recognize_google(speech, language="ko-KR")
            deque.append(audio)

        except sr.UnknownValueError:
            pass

        except sr.RequestError as e:
            pass

        except KeyboardInterrupt:
            break


# chatGPT 함수
def chatGPT(apiKey, model, speechs, deque):
    openai.api_key = apiKey

    print(f'ChatGPT Start')
    if speechs:
        query = speechs
        messages = [
            {"role": "system", "content": "You are a my firend."},
            {"role": "system", "content": "Please answer briefly"},
            {"role": "user", "content": query},
        ]
        response = openai.chat.completions.create(model=model, messages=messages)
        deque.append(response.choices[0].message.content)


# Text to Speech 함수
def text2Speech(apiKey, deque):
    openai.api_key = apiKey

    print(f'TTS Start')
    if deque:
        text = deque.popleft()
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )
        response.stream_to_file('./audio/output.mp3')
        

# python - arduino serial 통신 함수
def robotControl(deque):
    py_serial = serial.Serial(port='COM3', baudrate=9600,)

    print(f'Control Start')
    while True:
        if deque:
            commend = deque.popleft()
            py_serial.write(commend.encode())


# face detect 함수
def faceDetect(deque):
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(model_selection=1,  min_detection_confidence=0.9) as face_detection:
        cap = cv2.VideoCapture(0)

        print(f'Detect Start')
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Ignoring empty camera frame.")
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            h, w, _ = frame.shape
            # cv2.line(frame, (int(w/2-100), 0), (int(w/2-100), int(h)), (0, 0, 255), 2)
            # cv2.line(frame, (int(w/2+100), 0), (int(w/2+100), int(h)), (0, 0, 255), 2)

            if results.detections:
                bbox = results.detections[0].location_data.relative_bounding_box
                midpoint = (int((int(w * bbox.xmin) + int(w * bbox.xmin) + int(w * bbox.width))/2),
                                int((int(h * bbox.ymin) + int(h * bbox.ymin) + int(h * bbox.height))/2))
                # cv2.rectangle(frame, (int(w * bbox.xmin), int(h * bbox.ymin)),
                #                   (int(w * bbox.xmin) + int(w * bbox.width), int(h * bbox.ymin) + int(h * bbox.height)),
                #                   (0, 0, 255), 2)
                # cv2.circle(frame, midpoint, 2, (0, 0, 255), -1, cv2.LINE_AA)
                deque.append([w, midpoint])
            
            else:
                deque.append([w])

            # cv2.imshow('MediaPipe Face Detection', cv2.flip(frame, 1))

            # if cv2.waitKey(1) == ord('q'):
            #     cap.release()
            #     cv2.destroyAllWindows()
            #     break
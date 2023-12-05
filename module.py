from playsound import playsound
from collections import deque

import openai
import speech_recognition as sr


class cherrybot:
    def __init__(self, api, path, model):
        self.api = api
        self.path = path
        self.model = model

    # Speech To Text 함수
    def speechToText(self, deque):
        r = sr.Recognizer()

        while True:
            with sr.Microphone() as source:
                print("Say Something")
                speech = r.listen(source)

            try:
                audio = r.recognize_google(speech, language="ko-KR")
                print(audio)
                deque.append(audio)

            except sr.UnknownValueError:
                pass

            except sr.RequestError as e:
                pass

            except KeyboardInterrupt:
                break

    # 시간대별 인사 함수
    def timeToGreeting(self, time, greeting):
        if greeting:
            if time >= 5 and time <= 9:
                # 아침인사
                playsound(self.path + "morning.mp3")

            elif time >= 12 and time <= 13:
                # 점심 인사
                playsound(self.path + "lunch.mp3")

            elif time >= 19:
                # 저녁 인사
                playsound(self.path + "dinner.mp3")

            else:
                playsound(self.path + "hello.mp3")

        else:
            playsound(self.path + "bye.mp3")

    # GPT 함수
    def chatGPT(self, speech):
        openai.api_key = self.api

        model = self.model

        query = speech

        messages = [
            {"role": "system", "content": "You are a my firend."},
            {"role": "system", "content": "Please answer briefly"},
            {"role": "user", "content": query},
        ]

        response = openai.chat.completions.create(model=model, messages=messages)

        answer = response.choices[0].message.content

        return answer

    # Text to Speech 함수
    def textToSpeech(self, deque):
        openai.api_key = self.api

        if deque:
            text = deque.popleft()
            response = openai.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text,
            )

            response.stream_to_file(self.path + "output.mp3")

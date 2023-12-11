import speech_recognition as sr

# Speech To Text 함수
def speechToText(deque):
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
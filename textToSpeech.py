import openai
from playsound import playsound

# Text to Speech 함수
def textToSpeech(apiKey, deque):
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
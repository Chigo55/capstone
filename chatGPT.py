import openai

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
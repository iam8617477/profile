from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello how are you"},
    ],
)

print(completion.choices[0].message)
"""
ChatCompletionMessage(content="Hello! I'm here and ready to help you. How can I assist you today?", refusal=None, 
role='assistant', audio=None, function_call=None, tool_calls=None)
"""

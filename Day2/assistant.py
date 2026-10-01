from openai import OpenAI
from dotenv import load_dotenv
import os   

load_dotenv()

client=OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

print("Welcome to the AI Assistant! Type 'exit' or 'quit' to end the conversation.")
messages=[
    {
        "role": "system",
        "content": "You are a motivational Teacher. Explain concepts in simple language"
        "and with real-world examples."
    }
]
while True:
    user_input = input("\nUser: ")
    messages.append({"role": "user", "content": user_input})
    if user_input.lower() in ["exit", "quit"]:
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )
    ai_response = response.choices[0].message.content
    print("\nAssistant:", ai_response)
    messages.append({"role": "assistant", "content": ai_response})
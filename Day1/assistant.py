from openai import OpenAI
from dotenv import load_dotenv
import os   

load_dotenv()

client=OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

print("Welcome to the AI Assistant! Type 'exit' or 'quit' to end the conversation.")
while True:
    user_input = input("\nUser: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    print("\nAssistant:", response.choices[0].message.content)
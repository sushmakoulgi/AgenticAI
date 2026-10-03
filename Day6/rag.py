import dotenv 
import os
from openai import OpenAI
from retriever import load_documents_with_embedding,retrive_data


dotenv.load_dotenv()

client=OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))


documents=load_documents_with_embedding(client=client)


print("Welcome to the AI Assistant! Type 'exit' or 'quit' to end the conversation.")
while True:
    user_input = input("\nUser: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    context=retrive_data(user_input,client,documents)
    prompt=f" using the context {context}.answer the user question {user_input} using only this context"

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    print("\nAssistant:", response.choices[0].message.content)
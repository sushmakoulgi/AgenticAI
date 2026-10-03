from openai import OpenAI
import dotenv
import os
from similarity import cosine_similarity

dotenv.load_dotenv()

client=OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

response=client.embeddings.create(
    input="python is programming langauge",
    model="nomic-embed-text"
)
embedding1=response.data[0].embedding
print(type(embedding1))
print(len(embedding1))

response=client.embeddings.create(
    input="python is coding langauge",
    model="nomic-embed-text"
)
embedding2=response.data[0].embedding
print(type(embedding2))
print(len(embedding2))

print(cosine_similarity(embedding1,embedding2))
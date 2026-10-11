import os
import voyageai
from dotenv import load_dotenv

load_dotenv()


vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))


def get_embedding(message="hi",inputtype="document"):

    documents_embeddings = vo.embed(message, model="voyage-3.5", input_type=inputtype).embeddings

    # embed() returns one embedding per input; we pass a single string
    return documents_embeddings[0]

#get_embedding()
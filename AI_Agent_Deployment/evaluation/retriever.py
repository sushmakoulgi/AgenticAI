import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_voyageai import VoyageAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

loader=TextLoader(
    "notes.txt",
    encoding="utf-8"
)
splitter=RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

documents=loader.load()

chunks=splitter.split_documents(documents)

embeddings=VoyageAIEmbeddings(
    model="voyage-4",
    voyage_api_key=os.getenv("VOYAGE_API_KEY","")
)

# Embeds every chunk with Voyage and builds an in-memory FAISS index
vector_store=FAISS.from_documents(chunks, embeddings)

# Save to disk so the next run can FAISS.load_local(...) instead of re-embedding
vector_store.save_local("faiss_index")

retriever=vector_store.as_retriever(search_kwargs={"k":3})



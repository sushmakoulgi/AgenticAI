from pathlib import Path
from advanced_rag import build_rag,retrieve
from generator import generate_answer
import asyncio

DOCUMENT_PATH=(Path("documents")/"python.txt")


async def main():
    text=DOCUMENT_PATH.read_text(encoding='utf-8')
    print("Building RAG Knowledge base")
    build_rag(text,DOCUMENT_PATH.name)
    print("Advanced RAG is ready")

    while True:
        query=input("You: ").strip()

        if query.lower() =="quit":
            break

        results=await retrieve(query=query,top_k=5)

        print("retrieved Results")
        answer="Unable to Retrieve"
        if results:
            for result in results:
                print(f"source {result["source"]}, chunk = {result["text"]} Result-{result}")

            answer=await generate_answer(query,results)
        print(f"AI : {answer}")


asyncio.run(main())



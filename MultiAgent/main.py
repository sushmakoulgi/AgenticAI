from manager import run_manager
import asyncio

async def main():
    print("="*50)
    print("MULTI AGENT AI SYSTEM")
    print("="*50)

    task=input("Enter your task:  ")
    result=await run_manager(task)

    print("Agent : ")

    print("="*50)
    print("Here is the research \n",result["research"])
    print("="*50)

    print("="*50)
    print("Here is the code \n",result["code"])
    print("="*50)

    print("="*50)
    print("Here is the review \n",result["review"])
    print("="*50)


asyncio.run(main())
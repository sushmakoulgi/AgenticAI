import asyncio
from utils.validation import validate_task
from manager import run_manager
from utils.logger import logging


async def main():
    logging.info("="*50)
    logging.info("MULTI AGENT SYSTEM")
    logging.info("="*50)

    user_input=input("Enter your task:")

    task=validate_task(user_input)

    result=await run_manager(task)
    
    logging.info("Agent : ")
    
    logging.info("="*50)
    logging.info(f"Here is the research \n {result["research"]}")
    logging.info("="*50)

    logging.info("="*50)
    logging.info(f"Here is the code \n {result["code"]}")
    logging.info("="*50)

    logging.info("="*50)
    logging.info(f"Here is the review \n {result["review"]}")
    logging.info("="*50)



asyncio.run(main())


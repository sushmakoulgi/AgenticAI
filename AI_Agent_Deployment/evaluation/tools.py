from datetime import datetime
import random
import secrets
import string
from langchain_core.tools import tool
# from retriever import retriever
@tool
def get_current_timestamp() -> str:
    """Returns the current timestamp in YYYY-MM-DD_HH-MM-SS format."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 

@tool
def roll_dice(sides: int = 6) -> int:
    """Simulates rolling a dice with the given number of sides."""
    return random.randint(1, sides)

@tool
def generate_password(length=12):

    """ generate password on length provided in the arguements"""
    character=(string.ascii_letters+string.digits+string.punctuation)

    password="" 
    for i in range(length):
        password+=secrets.choice(character)
    return password

# @tool
# async def search_context(request):
#     """
#     for any request  on MCP related questions, returns the top results from 
#     notes"""
#     response=await retriever.ainvoke(request)
#     return response
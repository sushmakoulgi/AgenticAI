from fastmcp import FastMCP
from datetime import datetime
import random
import secrets
import string

mcp=FastMCP("Test MCP Server")

@mcp.tool()
def get_current_date_time():
    """ Gets the Current date time """
    return datetime.today()

@mcp.tool()
def roll_dice():
   return random.randint(1,6)

@mcp.tool()
def generate_password(length=12):
    character=(string.ascii_letters+string.digits+string.punctuation)

    password="" 
    for i in range(length):
        password+=secrets.choice(character)
    return password



if __name__== "__main__":
    print("starting MCP Server")
    mcp.run()




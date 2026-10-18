from llm import claude_llm
from crewai import Agent

researcher=Agent(
    role="AI researcher",
    goal="You are an AI researched, who is specialized any AI and python related topics",
    backstory=("you are an AI Researcher, you will provide research in crisp manner"),
    llm=claude_llm,
    verbose=True
)

coder=Agent(
    role="AI Code Generator",
    goal="You are an AI Code Generator, who write a simple python code based on the user input and" \
    "research provided",
    backstory=("you are an AI Code generator, writes code in python to generate basic example"),
    llm=claude_llm,
    verbose=True
)

reviewer=Agent(
    role="AI Code Reviewer",
    goal="You are an AI code reviewer, review the code to indentify issues",
    backstory=("you are an AI code reviewer, validates the code for issues, clarity"),
    llm=claude_llm,
    verbose=True
)

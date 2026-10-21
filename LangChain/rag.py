from model import model
from langchain_core.prompts import ChatPromptTemplate
from retriever import retriever
from langchain_core.output_parsers import StrOutputParser

prompt=ChatPromptTemplate.from_template(
    """ Answer the question by only using provided context
    context {context} and user question {question}
"""
)

def get_context(question):
    documents=retriever.invoke(question)
    return documents

chain=(
    {
        "context":get_context,
        "question":lambda x:x
    }
    |prompt
    |model
    |StrOutputParser()
)

response=chain.invoke("what is MCP")

print(response)
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "you are an AI assistance asnwer in maximum of  {max_sentences} sentences."),
    ("human", "{request}?"),
]).partial(max_sentences="2")




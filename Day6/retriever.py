from pathlib import Path
from tools import read_text_file,create_embedding
from similarity import cosine_similarity

def load_documents():
    documemt_location=Path("Knowledge")
    document_dict={}

    for file in Path.glob(documemt_location,"*.txt"):
        content=read_text_file(file)


    return document_dict


def load_documents_with_embedding(client):
    documemt_location=Path("Knowledge")
    document_dict={}
    
    for file in Path.glob(documemt_location,"*.txt"):
        content=read_text_file(file)
        document_dict[file]=create_embedding(content=content,client=client)
    
    return document_dict



def retrive_data(userinput:str,client,documents):
    user_question_embedding=create_embedding(userinput,client=client)
    max_score=0
    doc=None
    for filename,embedding in documents.items():
        score=cosine_similarity(embedding,user_question_embedding)
        print(f"score for {filename} is {score}")
        if score > max_score:
            doc=filename
            max_score=score

    return read_text_file(doc)



#testing

# dict=load_documents()

# def retriever(user_input:str):
#     user_input=user_input.lower()
#     for filename,content in dict.items():
#         if user_input in content.lower():
#             return filename
#     return None


# print("searching for python" ,retriever("Python"))
# print("searching for sql",retriever("sql"))
# print("searching for user",retriever("user"))
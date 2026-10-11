import json
import sqlite3
import numpy as np
from embedder import get_embedding

DATABASE="memory.db"


def create_database():
    connection=sqlite3.connect(database=DATABASE)
    cursor=connection.cursor()
    cursor.execute("""
 CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            assistant_message TEXT,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
""")

    cursor.connection.commit()
    connection.close()

def save_memory(user_request, assistant_response):
    message=user_request +"\n "+assistant_response
    embedding=get_embedding(message=message)
    connection=sqlite3.connect(DATABASE)
    cursor=connection.cursor()
    cursor.execute(
         """
              INSERT INTO memories
              (
                  user_message,
                  assistant_message,
                  embedding
              )
              VALUES (?, ?, ?)
              """,
              (
                  user_request,
                  assistant_response,
                  json.dumps(embedding)
              )
          )
    cursor.connection.commit()
    connection.close()

def search_semantic_memories(query, top_k=3, threshold=0.20):
    query_embedding=get_embedding(query,inputtype="query")
    connection=sqlite3.connect(DATABASE)
    cursor=connection.cursor()
    cursor.execute("""   SELECT
                user_message,
                assistant_message,
                embedding,
                created_at
            FROM memories
        """)
    
    rows = cursor.fetchall()
    
    connection.close()

    result=[]
    for (
        user_message,
                        assistant_message,
                        embedding,
                        created_at
    ) in rows:
       
        source_embedding=json.loads(embedding)
       
        score=cosine_similarity(source_embedding,query_embedding)
        if score >= threshold:
            result.append(
                {
                    "user_message":user_message,
                    "assistant_message":assistant_message,
                    "created_at":created_at,
                    "score":score
                }
            )

    result.sort(key=lambda item:item["score"],reverse=True)

    return result[:top_k]


def cosine_similarity(vector1,vector2):
    # flatten handles older rows saved as [[...]]
    vector1_array=np.array(vector1).flatten()
    vector2_array=np.array(vector2).flatten()

    prod=np.dot(vector1_array,vector2_array)

    return prod/(np.linalg.norm(vector1_array)* np.linalg.norm(vector2_array))


def save_semantic_memory(fact):
    embedding=get_embedding(fact,inputtype="query")
    connection=sqlite3.connect(DATABASE)
    cursor=connection.cursor()
    cursor.execute(
            """
                 INSERT INTO memories
                 (
                     user_message,
                     assistant_message,
                     embedding
                 )
                 VALUES (?, ?, ?)
                 """,
                 (
                     fact,
                     "",
                     json.dumps(embedding)
                 )
             )
    cursor.connection.commit()
    connection.close()
   

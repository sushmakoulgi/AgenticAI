from embedder import get_embedding
from chunker import create_chunks,embed_chunks
import numpy as np


def cosine_similarity(vector1,vector2):
    vector1_array=np.array(vector1)
    vector2_array=np.array(vector2)

    prod=np.dot(vector1_array,vector2_array)

    return prod/(np.linalg.norm(vector1_array)* np.linalg.norm(vector2_array))




def semantic_search(query,chunks,top_k=5):
    quesion_embedding=get_embedding(query)
    results=[]
    for chunk in chunks:
        similarity_score=cosine_similarity(quesion_embedding,chunk["embedding"])
        results.append(
            {
                "text":chunk["text"],
                "source":chunk["source"],
                "chunk_id":chunk["chunk_id"],
                "embedding": chunk["embedding"],
                "semantic_score":similarity_score
            }
        )
    results.sort(key=lambda item:item["semantic_score"],reverse=True)
    return results[:top_k]

def keyword_search(query,text):
    query_set=set(query.lower().split())
    text_set=set(text.lower().split())

    if len(query_set)==0:
        return 0.0

    match=query_set & text_set

    return len(match)/len(query_set)


def hybrid_search(query,chunks,top_k=5,semantic_weight=0.7, keyword_weight=0.3):
    quesion_embedding=get_embedding(query)
    results=[]
    for chunk in chunks:
        semantic_score=cosine_similarity(quesion_embedding,chunk["embedding"])
        keyword_score=keyword_search(query,chunk["text"])
        combined_score=(semantic_score*semantic_weight)+(keyword_score*keyword_weight)
        results.append(
            {
                "text":chunk["text"],
                "source":chunk["source"],
                "chunk_id":chunk["chunk_id"],
                "embedding": chunk["embedding"],
                "semantic_score":semantic_score,
                "keyword_score":keyword_score,
                "combined_score":combined_score
            }
        )

        results.sort(key=lambda item:item["combined_score"],reverse=True)
        return results[:top_k]
    
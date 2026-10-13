from chunker import create_chunks,embed_chunks
from reranker import rerank
from embedder import get_embedding
from chroma_store import add_chunks,search as chromasearch
from retriever import keyword_search

def build_rag(
        text,source
):
    chunks=create_chunks(text,source,chunk_size=200,overlap=50)
    embedded_chunks=embed_chunks(chunks=chunks)
    add_chunks(embedded_chunks)
    return embedded_chunks


async def retrieve(query,top_k):
    query_embedding=get_embedding(query)
    semantic_results=chromasearch(query_embedding,top_k)
    candidates=[]
    documents=semantic_results["documents"][0]
    metadatas=semantic_results["metadatas"][0]
    distances=semantic_results["distances"][0]

    for i in range(len(documents)):
        text=documents[i]
        metadata=metadatas[i]
        distance=distances[i]

        semantic_score=1/1+distance
        keyword_score=keyword_search(query=query,text=text)
        combined_score=(semantic_score*0.7)+(keyword_score*0.3)

        candidates.append(
            {
                "text":text,
                "source":metadata["source"],
                "chunk_id":metadata["chunk_id"],
                "semantic_score":semantic_score,
                "keyword_score":keyword_score,
                "combined_score":combined_score
            }
        )

        candidates.sort(key=lambda item:item["combined_score"],reverse=True)

        candidates=candidates[:top_k]

        return await rerank(query,candidates,3)


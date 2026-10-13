from embedder import get_embedding

def create_chunks(text,source, chunk_size=200, overlap=50):
    words=text.split()

    start=0
    chunk_id=0
    chunks=[]
    while start< len(words):
        end=start+chunk_size
        chunk_text=" ".join(words[start:end])
        chunks.append(
            {
                "text":chunk_text,
                "source":source,
                "chunk_id":chunk_id
            }
        )
        start=end-overlap
        chunk_id+=1
    return chunks

def embed_chunks(chunks:list):
    embedded_chunks=[]
    for chunk in chunks:
        embedding=get_embedding(chunk["text"])
        embedded_chunks.append(
            {
                "text":chunk["text"],
                "source":chunk["source"],
                "chunk_id":chunk["chunk_id"],
                "embedding": embedding
            })

    return embedded_chunks
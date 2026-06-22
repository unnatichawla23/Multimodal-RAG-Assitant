from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Generates embeddings for text chunks.

    Args:
        chunks (list): List of chunk dictionaries.

    Returns:
        list: List of chunk dictionaries with embeddings added.
    """
    chunk_texts = [chunk["chunk_text"] for chunk in chunks]

    embeddings = model.encode(chunk_texts)

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        chunk_with_embedding = chunk.copy()
        chunk_with_embedding["embedding"] = embedding.tolist()
        embedded_chunks.append(chunk_with_embedding)

    return embedded_chunks
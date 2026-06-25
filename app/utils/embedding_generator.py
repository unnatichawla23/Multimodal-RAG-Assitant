from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


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

def generate_query_embedding(query):
    """
    Generates an embedding for the user query.

    Args:
        query (str): Cleaned user question.

    Returns:
        list: Query embedding.
    """
    query_embedding = model.encode(query)

    return query_embedding.tolist()
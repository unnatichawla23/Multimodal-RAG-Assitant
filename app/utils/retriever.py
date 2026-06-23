from utils.vector_store import get_chroma_collection


def retrieve_relevant_chunks(query_embedding, top_k=5):
    """
    Retrieves the most relevant chunks from ChromaDB
    using the query embedding.

    Args:
        query_embedding (list): Embedding of the user question.
        top_k (int): Number of chunks to retrieve.

    Returns:
        list: Retrieved chunks with text and metadata.
    """
    collection = get_chroma_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        retrieved_chunks.append(
            {
                "chunk_text": document,
                "document_name": metadata["document_name"],
                "page_number": metadata["page_number"],
                "chunk_index": metadata["chunk_index"],
                "distance": distance
            }
        )

    return retrieved_chunks
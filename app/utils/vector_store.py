import chromadb
from config import CHROMA_DB_PATH, COLLECTION_NAME


def get_chroma_collection():
    """
    Creates or loads a persistent ChromaDB collection.

    Returns:
        ChromaDB collection object.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def store_embeddings_in_chroma(embedded_chunks):
    """
    Stores embedded chunks in ChromaDB.

    Args:
        embedded_chunks (list): List of chunks containing text, metadata, and embeddings.

    Returns:
        int: Number of chunks stored.
    """
    collection = get_chroma_collection()

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in embedded_chunks:
        chunk_id = (
            f"{chunk['document_name']}_"
            f"page_{chunk['page_number']}_"
            f"chunk_{chunk['chunk_index']}"
        )

        ids.append(chunk_id)
        documents.append(chunk["chunk_text"])
        embeddings.append(chunk["embedding"])
        metadatas.append(
            {
                "document_name": chunk["document_name"],
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"]
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(ids)

def clear_chroma_collection():
    """
    Clears the existing ChromaDB collection by deleting and recreating it.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection
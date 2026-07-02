import streamlit as st
from config import MAX_SOURCE_PREVIEW_LENGTH


def display_retrieved_sources(retrieved_chunks):
    """
    Displays retrieved document chunks as professional source citations.

    Args:
        retrieved_chunks (list): Retrieved chunks from ChromaDB.
    """
    st.subheader("📄 Sources")

    if not retrieved_chunks:
        st.warning("No relevant sources found.")
        return

    for index, chunk in enumerate(retrieved_chunks, start=1):
        with st.expander(
            f"Source {index}: {chunk['document_name']} | "
            f"Page {chunk['page_number']} | "
            f"Chunk {chunk['chunk_index']}"
        ):
            st.write(f"Document: {chunk['document_name']}")
            st.write(f"Page Number: {chunk['page_number']}")
            st.write(f"Chunk Index: {chunk['chunk_index']}")
            st.write(f"Similarity Distance: {round(chunk['distance'], 4)}")

            st.markdown("Source Preview")
            st.write(chunk["chunk_text"][:MAX_SOURCE_PREVIEW_LENGTH])
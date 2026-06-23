def build_rag_prompt(question, retrieved_chunks, mode):
    """
    Builds a structured RAG prompt using the user question,
    retrieved document chunks, and selected assistant mode.

    Args:
        question (str): Processed user question.
        retrieved_chunks (list): Relevant chunks retrieved from ChromaDB.
        mode (str): Selected assistant mode.

    Returns:
        str: Final prompt for the LLM.
    """
    context_blocks = []

    for chunk in retrieved_chunks:
        context_blocks.append(
            f"Source: {chunk['document_name']}, "
            f"Page: {chunk['page_number']}, "
            f"Chunk: {chunk['chunk_index']}\n"
            f"Content: {chunk['chunk_text']}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are SkillSight AI, a multimodal RAG-based Student and Career Assistant.

Selected Mode: {mode}

Answer the user's question using ONLY the provided document context.

Rules:
1. Do not use outside knowledge.
2. If the answer is not found in the context, say: "The answer is not available in the uploaded document."
3. Keep the answer clear, helpful, and student-friendly.
4. Mention source page numbers wherever relevant.
5. Do not hallucinate or invent information.

User Question:
{question}

Document Context:
{context}

Final Answer:
"""

    return prompt.strip()
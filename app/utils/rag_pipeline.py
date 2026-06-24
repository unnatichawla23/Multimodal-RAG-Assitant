from utils.file_handler import save_uploaded_file
from utils.pdf_processor import extract_text_from_pdf
from utils.ocr_processor import extract_text_from_image
from utils.text_chunker import create_text_chunks
from utils.embedding_generator import generate_embeddings, generate_query_embedding
from utils.vector_store import store_embeddings_in_chroma
from utils.retriever import retrieve_relevant_chunks
from utils.prompt_builder import build_rag_prompt
from utils.gemini_service import generate_answer_with_gemini


def run_rag_pipeline(uploaded_file, processed_question, mode):
    """
    Runs the complete RAG pipeline for an uploaded document and user question.
    """
    saved_file_path = save_uploaded_file(uploaded_file)

    file_type = uploaded_file.type

    if file_type == "application/pdf":
        extracted_pages = extract_text_from_pdf(saved_file_path)
        
    else:
        extracted_pages = extract_text_from_image(saved_file_path)

    if not extracted_pages:
        return {
            "success": False,
            "message": "No readable text found in this PDF."
        }

    chunks = create_text_chunks(
        pages_text=extracted_pages,
        document_name=uploaded_file.name
    )

    embedded_chunks = generate_embeddings(chunks)

    stored_count = store_embeddings_in_chroma(embedded_chunks)

    query_embedding = generate_query_embedding(processed_question)

    retrieved_chunks = retrieve_relevant_chunks(query_embedding)

    rag_prompt = build_rag_prompt(
        question=processed_question,
        retrieved_chunks=retrieved_chunks,
        mode=mode
    )

    final_answer = generate_answer_with_gemini(rag_prompt)

    return {
        "success": True,
        "saved_file_path": saved_file_path,
        "extracted_pages": extracted_pages,
        "chunks": chunks,
        "embedded_chunks": embedded_chunks,
        "stored_count": stored_count,
        "query_embedding": query_embedding,
        "retrieved_chunks": retrieved_chunks,
        "rag_prompt": rag_prompt,
        "final_answer": final_answer
    }
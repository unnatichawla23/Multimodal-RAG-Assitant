from utils.file_handler import save_uploaded_file
from utils.pdf_processor import extract_text_from_pdf
from utils.ocr_processor import extract_text_from_image
from utils.text_chunker import create_text_chunks
from utils.embedding_generator import generate_embeddings, generate_query_embedding
from utils.vector_store import store_embeddings_in_chroma, clear_chroma_collection
from utils.memory_manager import (
    documents_processed,
    set_documents_processed,
    reset_documents_processed,
    get_processed_files,
    set_processed_files,
    clear_processed_files
)
from utils.retriever import retrieve_relevant_chunks
from utils.prompt_builder import build_rag_prompt, build_quiz_prompt
from utils.gemini_service import generate_answer_with_gemini


def run_rag_pipeline(uploaded_files, processed_question, mode):
    """
    Runs the complete RAG pipeline for multiple uploaded documents and user question.
    """
    current_files = sorted([file.name for file in uploaded_files])
    processed_files = sorted(get_processed_files())

    uploaded_files_info = []
    all_extracted_pages = []
    all_chunks = []

    needs_processing = (
        not documents_processed()
        or current_files != processed_files
    )

    if needs_processing:
        clear_chroma_collection()

    for uploaded_file in uploaded_files:
        saved_file_path = save_uploaded_file(uploaded_file)

        file_info = {
            "file_name": uploaded_file.name,
            "file_type": uploaded_file.type,
            "file_size_kb": round(uploaded_file.size / 1024, 2),
            "saved_file_path": saved_file_path
        }

        uploaded_files_info.append(file_info)

        if uploaded_file.type == "application/pdf":
            extracted_pages = extract_text_from_pdf(saved_file_path)
        else:
            extracted_pages = extract_text_from_image(saved_file_path)

        if extracted_pages:
            chunks = create_text_chunks(
                pages_text=extracted_pages,
                document_name=uploaded_file.name
            )

            all_extracted_pages.extend(extracted_pages)
            all_chunks.extend(chunks)

    if not all_chunks:
        return {
            "success": False,
            "message": "No readable text found in the uploaded document(s)."
        }

    embedded_chunks = generate_embeddings(all_chunks)

    stored_count = store_embeddings_in_chroma(embedded_chunks)

    query_embedding = generate_query_embedding(processed_question)

    retrieved_chunks = retrieve_relevant_chunks(query_embedding)

    quiz_keywords = [
        "mcq",
        "mcqs",
        "quiz",
        "multiple choice",
        "practice question",
        "practice questions",
        "interview question",
        "interview questions",
        "viva question",
        "viva questions"
    ]

    if any(keyword in processed_question.lower() for keyword in quiz_keywords):
        rag_prompt = build_quiz_prompt(
            question=processed_question,
            retrieved_chunks=retrieved_chunks,
            mode=mode
        )
        
    else:
        rag_prompt = build_rag_prompt(
            question=processed_question,
            retrieved_chunks=retrieved_chunks,
            mode=mode
        )

    final_answer = generate_answer_with_gemini(rag_prompt)

    return {
        "success": True,
        "uploaded_files_info": uploaded_files_info,
        "extracted_pages": all_extracted_pages,
        "chunks": all_chunks,
        "embedded_chunks": embedded_chunks,
        "stored_count": stored_count,
        "query_embedding": query_embedding,
        "retrieved_chunks": retrieved_chunks,
        "rag_prompt": rag_prompt,
        "final_answer": final_answer
    }
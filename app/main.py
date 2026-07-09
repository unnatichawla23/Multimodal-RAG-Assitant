import streamlit as st

from utils.query_processor import process_user_query
from utils.rag_pipeline import run_rag_pipeline
from components.source_display import display_retrieved_sources
from utils.memory_manager import initialize_memory, add_to_memory, get_chat_history

from components.chat_interface import (
    get_user_message,
    display_user_message,
    display_assistant_message,
)

from components.quiz_display import display_quiz

st.set_page_config(
    page_title="SkillSight AI",
    page_icon="🧠",
    layout="wide"
)

initialize_memory()

# Welcome screen (shown only when no conversation exists)
if not get_chat_history():
    st.markdown("---")

    st.markdown("## 👋 Welcome to SkillSight AI")

    st.write(
        "Your AI-powered assistant for studying, research, resumes, career guidance, "
        "and document understanding."
    )

    st.markdown("### 💡 Try asking questions like:")

    st.markdown("""
    - 📄 Summarize this document
    - 🖼️ Explain this image
    - 📚 Explain this research paper in simple language
    - 📊 Compare these two documents
    - 📊 Compare two resumes
    - 📑 Compare two research papers
    - 📈 Compare two marksheets
    - 💼 Review my resume
    - 🎯 Suggest interview questions based on this resume
    """)

    st.markdown("---")

st.sidebar.title("🧠 SkillSight AI")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🤖 Assistant Settings")

mode = st.sidebar.selectbox(
    "Select Assistant Mode",
    [
        "Study Mode",
        "Research Mode",
        "Career Mode",
        "Image/Scanned Document Mode",
        "General Document Q&A Mode"
        "Document Comparison Mode"
    ]
)

developer_mode = st.sidebar.toggle(
    "Developer Mode",
    value=False
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload your document(s)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

question = get_user_message()


if question:
    st.subheader("Answer")

    chat_history = get_chat_history()

    # Display previous conversations
    for chat in chat_history:
        display_user_message(chat["question"])
        display_assistant_message(chat["answer"])

    # Display current question
    display_user_message(question)

    processed_question = process_user_query(question)

    if not processed_question:
        st.warning("Please enter a question before generating an answer.")
        st.stop()

    if not uploaded_files:
        st.warning("Please upload at least one document before asking a question.")
        st.stop()

    if (
        mode == "Document Comparison Mode"
        and len(uploaded_files) < 2
    ):
        st.warning(
            "Please upload at least two documents for comparison."
        )
        st.stop()

    if developer_mode:
        st.subheader("Processed Question")
        st.write(processed_question)

    result = run_rag_pipeline(
        uploaded_files=uploaded_files,
        processed_question=processed_question,
        mode=mode
    )

    if not result["success"]:
        st.warning(result["message"])
        st.stop()

    if developer_mode:
        st.success("File uploaded and processed successfully.")

        st.subheader("Uploaded File Details")

        for file_info in result["uploaded_files_info"]:
            st.write(f"File Name: {file_info['file_name']}")
            st.write(f"File Type: {file_info['file_type']}")
            st.write(f"File Size: {file_info['file_size_kb']} KB")
            st.write(f"Saved Path: {file_info['saved_file_path']}")
            st.divider()

    if developer_mode:
        st.subheader("Processing Summary")

        st.write(f"Extracted Pages: {len(result['extracted_pages'])}")
        st.write(f"Text Chunks Created: {len(result['chunks'])}")
        st.write(f"Embeddings Generated: {len(result['embedded_chunks'])}")
        st.write(f"Embedding Dimension: {len(result['query_embedding'])}")
        st.write(f"Chunks Stored in ChromaDB: {result['stored_count']}")

    if developer_mode:
        st.subheader("Retrieved Chunks")
        st.success(
            f"Retrieved {len(result['retrieved_chunks'])} relevant chunk(s) from ChromaDB."
        )

    if developer_mode:
        st.subheader("RAG Prompt Created")
        st.success("Structured prompt created successfully.")

        with st.expander("View Generated Prompt"):
            st.write(result["rag_prompt"])

    final_answer = result["final_answer"]

    if (
        "RESOURCE EXHAUSTED" in final_answer
        or "429" in final_answer
        or "quota exceeded" in final_answer.lower()
    ):
        st.error(final_answer)
        st.stop()

    if any(keyword in processed_question.lower() for keyword in [
        "mcq",
        "quiz",
        "multiple choice",
        "practice question",
        "interview question",
        "viva question"
    ]):
        
        display_quiz(result["final_answer"])
    else:
        display_assistant_message(final_answer)

    display_retrieved_sources(result["retrieved_chunks"])

    add_to_memory(
        processed_question,
        final_answer
    )
import streamlit as st

from utils.query_processor import process_user_query
from utils.rag_pipeline import run_rag_pipeline
from components.source_display import display_retrieved_sources
from utils.memory_manager import initialize_memory, add_to_memory, get_chat_history


st.set_page_config(
    page_title="SkillSight AI",
    page_icon="🧠",
    layout="wide"
)

initialize_memory()

st.title("🧠 SkillSight AI")
st.subheader("Multimodal RAG-based Student and Career Assistant")

st.write(
    "Upload PDFs, resumes, notes, research papers, screenshots, and scanned documents. "
    "Ask questions and get source-grounded answers."
)

st.sidebar.title("SkillSight AI")
st.sidebar.write("Choose how you want to use the assistant.")

mode = st.sidebar.selectbox(
    "Select Assistant Mode",
    [
        "Study Mode",
        "Research Mode",
        "Career Mode",
        "Image/Scanned Document Mode",
        "General Document Q&A Mode"
    ]
)

uploaded_file = st.file_uploader(
    "Upload your document",
    type=["pdf", "png", "jpg", "jpeg"]
)

question = st.text_area(
    "Ask a question about your uploaded document",
    placeholder="Example: Summarize this document in simple language."
)

submit_button = st.button("Generate Answer")

if submit_button:
    st.subheader("Answer")

    processed_question = process_user_query(question)

    if not processed_question:
        st.warning("Please enter a question before generating an answer.")
        st.stop()

    if uploaded_file is None:
        st.warning("Please upload a PDF document before asking a question.")
        st.stop()

    st.subheader("Processed Question")
    st.write(processed_question)

    result = run_rag_pipeline(
        uploaded_file=uploaded_file,
        processed_question=processed_question,
        mode=mode
    )

    if not result["success"]:
        st.warning(result["message"])
        st.stop()

    st.success("File uploaded and processed successfully.")

    st.subheader("Uploaded File Details")
    st.write(f"File Name: {uploaded_file.name}")
    st.write(f"File Type: {uploaded_file.type}")
    st.write(f"File Size: {round(uploaded_file.size / 1024, 2)} KB")
    st.write(f"Saved Path: {result['saved_file_path']}")

    st.subheader("Processing Summary")
    st.write(f"Extracted Pages: {len(result['extracted_pages'])}")
    st.write(f"Text Chunks Created: {len(result['chunks'])}")
    st.write(f"Embeddings Generated: {len(result['embedded_chunks'])}")
    st.write(f"Embedding Dimension: {len(result['query_embedding'])}")
    st.write(f"Chunks Stored in ChromaDB: {result['stored_count']}")

    st.subheader("Retrieved Chunks")
    st.success(
        f"Retrieved {len(result['retrieved_chunks'])} relevant chunk(s) from ChromaDB."
    )

    display_retrieved_sources(result["retrieved_chunks"])

    st.subheader("RAG Prompt Created")
    st.success("Structured prompt created successfully.")

    with st.expander("View Generated Prompt"):
        st.write(result["rag_prompt"])

    st.subheader("Final Answer")
    st.write(result["final_answer"])

    add_to_memory(processed_question, result["final_answer"])

    chat_history = get_chat_history()

    if chat_history:
        st.subheader("Conversation Memory")

        for index, chat in enumerate(chat_history, start=1):
            with st.expander(f"Chat {index}"):
                st.markdown("Question")
                st.write(chat["question"])

                st.markdown("Answer")
                st.write(chat["answer"])
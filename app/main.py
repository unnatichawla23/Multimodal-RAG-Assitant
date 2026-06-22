import streamlit as st
from utils.file_handler import save_uploaded_file
from utils.pdf_processor import extract_text_from_pdf
from utils.text_chunker import create_text_chunks
from utils.embedding_generator import generate_embeddings
from utils.vector_store import store_embeddings_in_chroma
from utils.query_processor import process_user_query

st.set_page_config(
    page_title="SkillSight AI",
    page_icon="🧠",
    layout="wide"
)

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
        

    st.subheader("Processed Question")
    st.write(processed_question)

    if uploaded_file is not None:
        saved_file_path = save_uploaded_file(uploaded_file)

        st.success("File uploaded and saved successfully.")

        st.subheader("Uploaded File Details")
        st.write(f"File Name: {uploaded_file.name}")
        st.write(f"File Type: {uploaded_file.type}")
        st.write(f"File Size: {round(uploaded_file.size / 1024, 2)} KB")
        st.write(f"Saved Path: {saved_file_path}")

        extracted_pages = extract_text_from_pdf(saved_file_path)

        st.subheader("Extracted Text Information")

        if extracted_pages:
            st.success(f"Extracted text from {len(extracted_pages)} page(s).")

            chunks = create_text_chunks(
                pages_text=extracted_pages,
                document_name=uploaded_file.name
            )

            st.subheader("Text Chunks Created")
            st.success(f"Created {len(chunks)} chunk(s).")

            embedded_chunks = generate_embeddings(chunks)

            st.subheader("Embeddings Generated")
            st.success(
                f"Generated embeddings for {len(embedded_chunks)} chunk(s)."
            )

            st.write(
                f"Embedding dimension: "
                f"{len(embedded_chunks[0]['embedding'])}"
            )

            stored_count = store_embeddings_in_chroma(embedded_chunks)
            st.subheader("Vector Database Storage")
            st.success(f"Stored {stored_count} chunk(s) in ChromaDB.")

            st.subheader("Chunk Preview")

            for chunk in chunks[:3]:
                st.markdown(
                    f"**Chunk {chunk['chunk_index']}** | "
                    f"Document: {chunk['document_name']} | "
                    f"Page: {chunk['page_number']}"
                )

                st.write(chunk["chunk_text"][:700])

        else:
            st.warning("No readable text found in this PDF.")

    else:
        st.warning("Please upload a PDF document before asking a question.")
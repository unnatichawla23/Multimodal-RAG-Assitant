import streamlit as st
from utils.file_handler import save_uploaded_file
from utils.pdf_processor import extract_text_from_pdf

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

    if uploaded_file is not None:
        saved_file_path = save_uploaded_file(uploaded_file)

        st.success("File uploaded and saved successfully.")

        st.subheader("Uploaded File Details")
        st.write(f"File Name: {uploaded_file.name}")
        st.write(f"File Type: {uploaded_file.type}")
        st.write(f"File Size: {round(uploaded_file.size / 1024, 2)} KB")
        st.write(f"Saved Path: {saved_file_path}")

        extracted_pages = extract_text_from_pdf(saved_file_path)

        st.subheader("Extracted Text Preview")

        if extracted_pages:
            st.success(f"Extracted text from {len(extracted_pages)} page(s).")

            for page in extracted_pages[:2]:
                st.markdown(f"Page {page['page_number']}")
                st.write(page["text"][:1000])
        else:
            st.warning("No readable text found in this PDF.")
    else:
        st.warning("Please upload a PDF document before asking a question.")
import streamlit as st

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
    st.info("AI answer will appear here in upcoming sessions.")

    st.subheader("Selected Mode")
    st.write(mode)

    if uploaded_file is not None:
        st.subheader("Uploaded File")
        st.write(uploaded_file.name)
    else:
        st.warning("Please upload a document before asking a question.")
def initialize_memory():
    """
    Creates conversation memory if it doesn't exist.
    """
    import streamlit as st

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def add_to_memory(
    question,
    answer,
    mode,
    retrieved_chunks
):
    """
    Stores a question-answer pair in memory.
    """
    import streamlit as st

    st.session_state.chat_history.append(
        {
            "question": question,
            "answer": answer,
            "mode": mode,
            "retrieved_chunks": retrieved_chunks
        }
    )


def get_chat_history():
    """
    Returns stored conversation history.
    """
    import streamlit as st

    return st.session_state.chat_history


def set_documents_processed(value):
    """
    Stores whether the current uploaded documents
    have already been processed.
    """
    import streamlit as st

    st.session_state.documents_processed = value


def documents_processed():
    """
    Returns processing status.
    """
    import streamlit as st

    return st.session_state.get("documents_processed", False)


def reset_documents_processed():
    """
    Resets processing status.
    """
    import streamlit as st

    st.session_state.documents_processed = False

def set_processed_files(file_names):
    """
    Stores the filenames of the currently processed documents.
    """
    import streamlit as st

    st.session_state.processed_files = file_names


def get_processed_files():
    """
    Returns the filenames of the currently processed documents.
    """
    import streamlit as st

    return st.session_state.get("processed_files", [])


def clear_processed_files():
    """
    Clears the processed filenames.
    """
    import streamlit as st

    st.session_state.processed_files = []

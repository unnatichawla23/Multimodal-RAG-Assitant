def initialize_memory():
    """
    Creates conversation memory if it doesn't exist.
    """
    import streamlit as st

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def add_to_memory(question, answer):
    """
    Stores a question-answer pair in memory.
    """
    import streamlit as st

    st.session_state.chat_history.append(
        {
            "question": question,
            "answer": answer
        }
    )


def get_chat_history():
    """
    Returns stored conversation history.
    """
    import streamlit as st

    return st.session_state.chat_history
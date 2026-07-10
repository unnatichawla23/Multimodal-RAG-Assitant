import streamlit as st


def display_suggested_questions(questions):
    """
    Displays suggested follow-up questions.
    """

    if not questions:
        return

    st.markdown("### 💡 Suggested Questions")

    for question in questions:
        st.markdown(f"- {question}")
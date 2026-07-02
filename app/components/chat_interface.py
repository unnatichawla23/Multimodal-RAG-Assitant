import streamlit as st


def get_user_message():
    
    return st.chat_input("Ask SkillSight AI anything about your uploaded documents...")


def display_user_message(message):
    
    with st.chat_message("user"):
        st.markdown(message)


def display_assistant_message(message):
    
    with st.chat_message("assistant"):
        st.markdown(message)


import streamlit as st
from gemini_app import get_qa_chain, create_vector_db

def app():
    try:
        # Check if the user is logged in by checking the presence of 'username' in session state
        if 'username' not in st.session_state or st.session_state.username == '':
            st.text('Please Login first')
            return
        
        create_vector_db()
        st.title("Prompt For Better Education!")
        
        # Initialize chat history
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        question = st.text_input("Question: ")

        if question:
            chain = get_qa_chain()
            response = chain(question)

            # Append the new question and response to the history
            st.session_state['history'].append((question, response["result"]))

        st.header("Answer")

        # Display the chat history
        for q, a in st.session_state['history']:
            st.write(f"**Question:** {q}")
            st.write(f"**Answer:** {a}")
            st.write("---")  # Separator for readability

    except Exception as e:
        st.text(f"An error occurred: {str(e)}")
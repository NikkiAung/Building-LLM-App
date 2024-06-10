import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import os

cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_admin.initialize_app(cred)

def app():
    db = firestore.client()

    try:
        st.title('Posted by: ' + st.session_state['username'])

        # Fetch posts
        result = db.collection('Posts').document(st.session_state['username']).get()
        r = result.to_dict()
        content = r['Content']

        def delete_post(k):
            c = int(k)
            h = content[c]
            try:
                db.collection('Posts').document(st.session_state['username']).update({"Content": firestore.ArrayRemove([h])})
                st.warning('Post deleted')
            except:
                st.write('Something went wrong..')

        # Display posts
        for c in range(len(content) - 1, -1, -1):
            st.text_area(label='', value=content[c])
            st.button('Delete Post', on_click=delete_post, args=([c]), key=c)

        # Fetch chat history
        chat_history = db.collection('Chats').document(st.session_state['username']).get()
        chat_data = chat_history.to_dict()
        chats = chat_data.get('Messages', [])

        st.subheader('Chat History')
        for chat in chats:
            st.text_area(label='', value=chat, height=100)

    except:
        if st.session_state.username == '':
            st.text('Please Login first')

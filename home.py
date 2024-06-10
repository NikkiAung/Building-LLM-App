import streamlit as st
from firebase_admin import firestore, credentials
import firebase_admin
import os
from dotenv import load_dotenv
load_dotenv()

def app():
    # Check if Firebase Admin SDK is initialized, and initialize it if not
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        firebase_admin.initialize_app(cred)

    # Initialize session state variables if not present
    if 'username' not in st.session_state:
        st.session_state.username = ''

    if 'db' not in st.session_state:
        st.session_state.db = firestore.client()

    db = st.session_state.db
    
    ph = ''
    if st.session_state.username == '':
        ph = 'Login to be able to post!!'
    else:
        ph = 'Feel Free To Post Here If You Wanna Contribute/Suggest To Professors Chosen By Burmese Seniors Data Base 🫡'

    post = st.text_area(label=' :orange[+ New Post]', placeholder=ph, height=None, max_chars=500)
    if st.button('Post', use_container_width=True):
        if st.session_state.username == '':
            st.error('Please login first to post!')
        elif post != '':
            try:
                info = db.collection('Posts').document(st.session_state.username).get()
                if info.exists:
                    info = info.to_dict()
                    if 'Content' in info.keys():
                        pos = db.collection('Posts').document(st.session_state.username)
                        pos.update({u'Content': firestore.ArrayUnion([u'{}'.format(post)])})
                    else:
                        data = {"Content": [post], 'Username': st.session_state.username}
                        db.collection('Posts').document(st.session_state.username).set(data)
                else:
                    data = {"Content": [post], 'Username': st.session_state.username}
                    db.collection('Posts').document(st.session_state.username).set(data)
                    
                st.success('Post uploaded!!')
            except Exception as e:
                st.error(f'Error uploading post: {e}')
    
    st.header(' :violet[Latest Posts] ')
    
    try:
        docs = db.collection('Posts').get()
        
        for doc in docs:
            d = doc.to_dict()
            try:
                st.markdown("""
                    <style>
                    .stTextArea [data-baseweb=base-input] [disabled=""]{
                        -webkit-text-fill-color: white;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                
                st.text_area(label=':green[Posted by:] ' + ':orange[{}]'.format(d['Username']), 
                             value=d['Content'][-1], height=20, disabled=True)
            except:
                pass
    except Exception as e:
        st.error(f'Error fetching posts: {e}')
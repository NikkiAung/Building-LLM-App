import streamlit as st
import firebase_admin
from firebase_admin import firestore

def app():
    # Check if Firebase Admin SDK is initialized, and initialize it if not
    if not firebase_admin._apps:
        firebase_admin.initialize_app()

    if 'db' not in st.session_state:
        st.session_state.db = ''

    db = firestore.client()
    st.session_state.db = db
    
    ph = ''
    if st.session_state.username == '':
        ph = 'Login to be able to post!!'
    else:
        ph = 'Post your thought'    

    post = st.text_area(label=' :orange[+ New Post]', placeholder=ph, height=None, max_chars=500)
    if st.button('Post', use_container_width=20):
        if post != '':
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
    
    st.header(' :violet[Latest Posts] ')
    
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
            
            st.text_area(label=':green[Posted by:] '+':orange[{}]'.format(d['Username']), 
                         value=d['Content'][-1], height=20, disabled=True)
        except:
            pass

url =''

import streamlit as st

def app():
    st.subheader('Show your support by buying me a coffee!')
    st.markdown(f'<a href="{url}" target="_blank" style="background-color: #008CBA; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">Donate</a>', unsafe_allow_html=True)
    st.write("The donation link is still under construction")
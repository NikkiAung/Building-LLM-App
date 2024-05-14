import streamlit as st

from streamlit_option_menu import option_menu

import about, account, home, trending, your_posts, buymeCoffee

st.set_page_config(
    page_title="Rate My Professor"
)

class MultiApp:

    def __init__(self):
        self.apps = []
    
    
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
    
    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Rate My Professor ',
                options=['Home','Account','Trending','Your Posts','About','Buy_me_a_coffee'],
                icons=['house-fill','person-circle','trophy-fill','chat-fill','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "10px !important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )
            
        if app == 'Home':
            home.app()
        if app == 'Account':
            account.app()
        if app == 'Trending':
            trending.app()
        if app == 'About':
            about.app()
        if app == 'Your Posts':
            your_posts.app()
        if app == 'Buy_me_a_coffee':
            buymeCoffee.app()
    run()
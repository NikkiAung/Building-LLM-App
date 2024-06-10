import streamlit as st

from streamlit_option_menu import option_menu

import about, account, home, your_posts, buymeCoffee, langchain_helper

st.set_page_config(
    page_title="Burmese Seniors Guidelines"
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
                menu_title='Go Try Every Feature Listed Below! ✌️',
                options=['Account','Home','Your Posts','CHAT-BOT','Funds-For-Club','About'],
                icons=['person-circle','house-fill','chat-fill','robot','bi-currency-dollar','info-circle-fill'],
                default_index=1,
                styles={
                    "container": {"padding": "10px !important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}    
                )
        if app == 'Account':
            account.app()
        if app == 'Home':
            home.app()
        if app == 'Your Posts':
            your_posts.app()
        if app == 'CHAT-BOT':
            langchain_helper.app()
        if app == 'Funds-For-Club':
            buymeCoffee.app()
        if app == 'About':
            about.app()
    run()
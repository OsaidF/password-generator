import streamlit as st
import string
import random
from st_copy_to_clipboard import st_copy_to_clipboard


st.set_page_config(
    page_title="Password Generator",
    page_icon=":1234:",
    layout="centered"
)
    
if "password" not in st.session_state:
    st.session_state.password = ""

def app():
    st.header(':sparkles: Password Generator & Strength Checker _by :red[Osaid]_')
    st.subheader("Test your own password:")
    user_input = st.text_input("Test your own password:", value=st.session_state.password, label_visibility= "hidden")
    if user_input:
        if user_input != st.session_state.password:
            st.session_state.password = user_input

    hr = st.container()
    left, center, right = hr.columns([3,1,3])
    left.divider()
    right.divider()
    center.markdown("<h3 style='display: flex; justify-content: center; align-tems: center; padding-bottom:0px'>OR</h3>", unsafe_allow_html=True)
    st.subheader("Generate a password:")
    begin = st.container()
    column1, column2 = begin.columns([3, 1])
    butt1, butt2, butt3 = column2.columns(3)
    my_bar = begin.progress(0)

    col1, col2, col3 = st.columns(3)
    length = len(st.session_state.password)
    with col1:
        length = st.slider(
        "Password Length:", 1, 15, value = length,
        )
        st.text(length)
    with col2:
        radio = st.radio(
            "Password Type:",
            key="type",
            options=["Easy to read", "All Characters"],
            index=1
        )

    with col3:
        st.caption('Options:')
        if radio == 'Easy to read':
            uppercase = st.checkbox(
                "Uppercase", key="uppercase", value = True
            )

            lowercase = st.checkbox(
                "Lowercase", key="lowercase", value = True
            )
            numbers = st.checkbox(
                "Numbers", key="e_numbers", value = False, disabled = True 
            )
            symbols = st.checkbox(
                "Symbols", key="e_symbols", value = False, disabled = True
            )

        else:
            uppercase = st.checkbox(
                "Uppercase", key="uppercase", value= True
            )

            lowercase = st.checkbox(
                "Lowercase", key="lowercase", value="true"
            )
            numbers = st.checkbox(
                "Numbers", key="numbers", value="true", 
            )

            symbols = st.checkbox(
                "Symbols", key="symbols", value="true"
            )

    population = []
    if 'passwords' not in st.session_state:
        st.session_state.passwords = []

    if uppercase == True:
        population.append(string.ascii_uppercase)
    if lowercase == True:
        population.append(string.ascii_lowercase)
    if numbers == True:
        population.append(string.digits)
    if symbols == True:
        population.append(string.punctuation)

    if len(population) > 0:
        single_string = "".join(population)
        def gen_pass(): 
            password = ''.join(random.choices( single_string ,k=length))
            st.session_state.password = password
        def progress_bar():
            score = 0
            length = len(st.session_state.password)
            upper_case = any(c.isupper() for c in st.session_state.password)
            lower_case = any(c.islower() for c in st.session_state.password)
            special = any(c in string.punctuation for c in st.session_state.password)
            digits = any(c.isdigit() for c in st.session_state.password)

            characters = [upper_case, lower_case, special, digits]

            if length > 6:
                score += 1
            if length > 8:
                score += 1
            if length > 10:
                score += 1
            if length > 14:
                score += 1

            score += sum(characters) - 1

            if score < 4:
                my_bar.progress(30, text=f'Weak Password! Score: {score}')
            elif score == 4:
                my_bar.progress(50, text=f'Medium Password! Score: {score}')
            elif 4 < score < 6:
                my_bar.progress(80, text=f'Strong Password! Score: {score}')
            else:
                my_bar.progress(100, text=f'Very Strong Password! Score: {score}')
        progress_bar()
        column1.header(st.session_state.password)

        def append_item(item):
            if len(st.session_state.passwords) == 5:
                st.session_state["passwords"].pop(4)
                st.session_state["passwords"].insert(0, item)
            else:
                st.session_state["passwords"].insert(0, item)
        def multi_func(item):
            gen_pass()
            append_item(item)
            

        butt2.button('🔁', on_click=multi_func, args= [st.session_state.password])
        with butt1:
            st_copy_to_clipboard(st.session_state.password)


    else:
        begin.header('Select one of the options!')

    if len(st.session_state.passwords) > 0:
        st.subheader('Previous generated passwords:')
        for x in st.session_state.passwords:
            st.text(x)

    st.header(st.session_state)

if __name__ == "__main__":
    app()
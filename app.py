import streamlit as st
import string
import random
from st_copy_to_clipboard import st_copy_to_clipboard


def app():
    st.header(':sparkles: Password Generator _by :red[Osaid]_')
    st.markdown('''#### Inspired by [LastPass Password Generator.](https://www.lastpass.com/features/password-generator) :1234: &mdash;\
                

Creates a strong, unique passwords with customizable options, including length, special characters, and numbers.🎯 
It ensures randomness for maximum security against hacking attempts🎉🚀.  
''')
    begin = st.container()
    column1, column2 = begin.columns([3, 1])
    butt1, butt2, butt3 = column2.columns(3)
    my_bar = begin.progress(0)

    col1, col2, col3 = st.columns(3)
    length = 8
    with col1:
        length = st.slider(
        "Password Length:", 1, 15, value = length
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
            return password
        password = gen_pass()
        def progress_bar():
            score = 0
            length = len(password)
            upper_case = any(c.isupper() for c in password)
            lower_case = any(c.islower() for c in password)
            special = any(c in string.punctuation for c in password)
            digits = any(c.isdigit() for c in password)

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
                my_bar.progress(30, text='Weak Password!')
            elif score == 4:
                my_bar.progress(50, text='Medium Password!')
            elif 4 < score < 6:
                my_bar.progress(80, text='Strong Password!')
            else:
                my_bar.progress(100, text='Very Strong Password!')
            
            # if len(password) > 11:
            #     my_bar.progress(100, text='Impossible to crack!')
            # elif len(password) > 8:
            #     my_bar.progress(80, text='Very Strong!')
            # elif len(password) > 6:
            #     my_bar.progress(50, text='Medium Strength')
            # elif len(password) > 3:
            #     my_bar.progress(30, text='Weak Password')
            # elif len(password) < 1:
            #     my_bar.progress(0)
        progress_bar()
        column1.header(password)

        def append_item(item):
            if len(st.session_state.passwords) == 5:
                st.session_state["passwords"].pop(4)
                st.session_state["passwords"].insert(0, item)
            else:
                st.session_state["passwords"].insert(0, item)

        butt2.button('🔁', on_click= append_item, args= [password])
        with butt1:
            st_copy_to_clipboard(password)


    else:
        begin.header('Select one of the options!')

    if len(st.session_state.passwords) > 0:
        st.subheader('Previous generated passwords:')
        for x in st.session_state.passwords:
            st.text(x)

if __name__ == "__main__":
    app()
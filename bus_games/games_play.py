import streamlit as st

# Text Elements
st.title("My App Title")
st.write("This is a simple text description.")

# Input Widgets
user_name = st.text_input("Enter your name:")
click_me = st.button("Submit Data")

# Interactive Response
if click_me:
    st.write(f"Hello, {user_name}!")

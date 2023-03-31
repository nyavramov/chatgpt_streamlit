import openai
import streamlit as st

from streamlit_chat import message

openai.api_key = st.secrets["OPENAI_TOKEN"]


def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly and helpful bot that "
                                          "attempts to assist the user with whatever "
                                          "questions they may have"},
            {"role": "user", "content": prompt},
        ]
    )

    return response['choices'][0]["message"]["content"]


st.title("ChatGPT Web App")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = st.text_input("You:", key='input')

if user_input:
    output = generate_response("User: " + user_input + "\nBot: ")
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
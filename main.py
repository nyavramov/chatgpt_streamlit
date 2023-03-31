import openai
import streamlit as st

from streamlit_chat import message

openai.api_key = st.secrets["OPENAI_TOKEN"]


def generate_response(prompt: str) -> str:
    st.session_state['messages'].append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages'],
    )

    bot_response = response['choices'][0]["message"]["content"]

    st.session_state['messages'].append(
        {"role": "assistant", "content": bot_response})

    return bot_response


st.title("ChatGPT Web App")

if 'chat_log' not in st.session_state:
    st.session_state['chat_log'] = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
            {"role": "system", "content": "You are a friendly and helpful bot that "
                                          "attempts to assist the user with whatever "
                                          "questions they may have"},
        ]

user_input = st.text_input("You:", key='input')

if user_input:
    bot_response = generate_response("User: " + user_input + "\nBot: ")
    st.session_state['chat_log'].append((user_input, bot_response))


if st.session_state['chat_log']:
    # Loop through the chat messages directly without reversing
    for i, (user_message, bot_message) in enumerate(st.session_state['chat_log']):
        message(user_message, is_user=True, key=str(i) + '_user')
        message(bot_message, key=str(i))

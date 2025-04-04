import streamlit as st
from openai import OpenAI

st.title("✨ 나만의 코드 도우미 챗봇")

api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
if not api_key:
    st.info("API 키를 입력하세요!")
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    messages = [{"role": "system", "content": "너는 코드 도우미 챗봇이야."}]
    messages += [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

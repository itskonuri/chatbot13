import streamlit as st
from openai import OpenAI

st.title("💬 Code editor")
st.write("Konuri's code editor — it is only for Konuri!")

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # 최신 openai 라이브러리 기준
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        messages = [{"role": "system", "content": "너는 코드 수정에 특화된 헬퍼야."}]
        messages += [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )

            with st.chat_message("assistant"):
                response = st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")

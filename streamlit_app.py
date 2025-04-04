import streamlit as st
from openai import OpenAI

st.title("💬 Code editor")
st.write("Konuri's code editor — it is only for Konuri!")

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # ✅ 클라이언트 객체 생성 (OpenAI v1 기준)
    client = OpenAI(api_key=openai_api_key)

    # 세션 메시지 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 대화 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 전체 메시지 리스트 준비 (시스템 + 이전 메시지)
        messages = [{"role": "system", "content": "너는 코드 수정에 특화된 헬퍼야."}]
        messages += [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        # 🔥 올바른 Chat API 호출
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True
            )

            with st.chat_message("assistant"):
                response = st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"❌ 에러 발생: {e}")

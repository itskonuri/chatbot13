import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Code editor")
st.write(
    "Konuri's code editor\n"
    "It is only for Konuri 🛠️"
)

# Ask user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client using the v1 style
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input field
    if prompt := st.chat_input("What is up?"):
        # Append user's message to session
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare messages for the API (prepend system prompt)
        messages = [{"role": "system", "content": "너는 코드 수정에 특화된 헬퍼야."}]
        messages += [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        # Generate a response from OpenAI
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )

            # Display and store the response
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"❌ 에러 발생: {e}")

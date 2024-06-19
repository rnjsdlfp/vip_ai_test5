import openai
import streamlit as st

# Sidebar for API key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

# Title and caption
st.title("💬 VIP AI")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Initialize messages if not in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    st.write(f"**{role.capitalize()}:** {msg['content']}")

# Handle user input
prompt = st.text_input("Your message:", "")
if st.button("Send"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    try:
        # Initialize OpenAI client
        openai.api_key = openai_api_key

        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.write(f"**User:** {prompt}")

        # Prepare messages for the API call
        messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ]

        # Request response from ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace "gpt-4o" with "gpt-3.5-turbo" or "gpt-4" if applicable
            messages=messages
        )

        # Extract and display assistant's response
        msg = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.write(f"**Assistant:** {msg}")

    except Exception as e:
        st.error(f"An error occurred: {e}")



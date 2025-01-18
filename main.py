import streamlit as st
import requests

# Retrieve secrets from the secrets.toml file
LANGFLOW_ID = st.secrets["LANGFLOW_ID"]
FLOW_ID = st.secrets["FLOW_ID"]
APPLICATION_TOKEN = st.secrets["APPLICATION_TOKEN"]

# Base URL for the Langflow API
BASE_API_URL = f"https://api.langflow.astra.datastax.com/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"

# Function to run the flow
def run_flow(input_message):
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "input_value": input_message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "ChatInput-ivyVt": {},
            "Prompt-lpeoJ": {},
            "ChatOutput-eV0ob": {},
            "OpenAIModel-SzTnW": {}
        }
    }
    response = requests.post(BASE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Streamlit app setup
st.set_page_config(page_title="DIU Support Bot", layout="wide")
st.title("DIU Support Bot")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
prompt = st.chat_input("Type your message here...")
if prompt:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get response from Langflow
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = run_flow(prompt)
                assistant_message = result['outputs'][0]['outputs'][0]['results']['message']['text']
                st.write(assistant_message)
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    except Exception as e:
        st.error(f"Error: {e}")

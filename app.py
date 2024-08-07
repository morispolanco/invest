import streamlit as st
import requests
import json

# Streamlit app title
st.title("Investigator Agent")

# Function to call the Together API
def call_together_api(prompt, temperature, top_p, top_k, max_tokens):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['TOGETHER_API_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "repetition_penalty": 1,
        "stop": ["<|eot_id|>"],
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Sidebar for advanced settings
st.sidebar.header("Advanced Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.7, 0.1)
top_k = st.sidebar.slider("Top K", 1, 100, 50, 1)
max_tokens = st.sidebar.slider("Max Tokens", 100, 1000, 912, 50)

# User input
user_query = st.text_input("Enter your research question:")

if user_query:
    if st.button("Investigate"):
        with st.spinner("Investigating..."):
            result = call_together_api(
                f"Act as an investigator and research the following question: {user_query}",
                temperature,
                top_p,
                top_k,
                max_tokens
            )
        st.write("Investigation Results:")
        st.write(result)

# Instructions for use
st.sidebar.header("Instructions for Use")
st.sidebar.info(
    "To use this application, simply enter your research question in the text field and press the 'Investigate' button. "
    "The application will use the Together API to investigate and provide relevant results. "
    "You can adjust the advanced settings in the sidebar to fine-tune the AI's response."
)

# Explanation of advanced settings
st.sidebar.header("Advanced Settings Explanation")
st.sidebar.info(
    "**Temperature:** Controls randomness. Higher values make output more random, lower values make it more focused and deterministic.\n\n"
    "**Top P:** Nucleus sampling. It sets the cumulative probability cutoff for token selection.\n\n"
    "**Top K:** Limits the number of tokens considered for each step.\n\n"
    "**Max Tokens:** The maximum number of tokens to generate in the response."
)

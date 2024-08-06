import streamlit as st
import requests

# Streamlit app title
st.title("Investigator Agent")

# Function to call the Together API
def call_together_api(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['TOGETHER_API_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 912,
        "temperature": 0,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": [""],
        "stream": False  # Changed to False for simplicity
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# User input
user_query = st.text_input("Enter your research question:")

if user_query and st.button("Investigate"):
    with st.spinner("Investigating..."):
        result = call_together_api(f"Act as an investigator and research the following question: {user_query}")
        st.write("Investigation Results:")
        st.write(result)

# Instructions for setting up the secret
st.sidebar.header("Setup Instructions")
st.sidebar.info(
    "To use this app, you need to set up your Together API key in Streamlit's secrets. "
    "Create a file named `.streamlit/secrets.toml` in your app's root directory and add the following line:\n\n"
    "TOGETHER_API_KEY = 'your_api_key_here'\n\n"
    "Replace 'your_api_key_here' with your actual Together API key."
)

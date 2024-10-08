import streamlit as st
import requests
import json

# Streamlit app title
st.title("Investigator Agent")

# Function to call the Together API
def call_together_api(prompt):
    # Agregar filtro para limitar la investigación a la legislación guatemalteca
    if "Guatemala" not in prompt and "legislación guatemalteca" not in prompt:
        prompt += " en el contexto de la legislación guatemalteca"
    
    # Agregar URL del sitio web de Guatemala Justia
    prompt += " en el sitio web de Guatemala Justia (https://guatemala.justia.com)"
    
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
        "stop": ["\n"],
        "stream": False  # Changed to False for simplicity
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# User input
user_query = st.text_input("Enter your research question:")
if user_query:
    if st.button("Investigate"):
        with st.spinner("Investigating..."):
            result = call_together_api(f"Act as an investigator and research the following question: {user_query}")
        st.write("Investigation Results:")
        st.write(result)

# Instructions for use
st.sidebar.header("Instructions for Use")
st.sidebar.info(
    "To use this application, simply enter your research question in the text field and press the 'Investigate' button. "
    "The application will use the Together API to investigate and provide relevant results."
)

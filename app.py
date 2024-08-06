import streamlit as st
import requests
import json

# Título de la aplicación de Streamlit
st.title("Agente Investigador")

# Función para llamar a la API de Together
def llamar_api_together(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['TOGETHER_API_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1912,
        "temperature": 0.5,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["\""],
        "stream": False  # Cambiado a False para simplificar
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Entrada del usuario
consulta_usuario = st.text_input("Ingrese su pregunta de investigación:")

if consulta_usuario:
    if st.button("Investigar"):
        with st.spinner("Investigando..."):
            resultado = llamar_api_together(f"Actúa como un investigador y investiga la siguiente pregunta: {consulta_usuario}. ")
            st.write("Resultados de la investigación:")
            st.write(resultado)

# Instrucciones para configurar el secreto
st.sidebar.header("Acerca de")
st.sidebar.info(
    "Esta aplicación utiliza Meta-Llama-3.1-405B-Instruct-Turbo para investigar y responder a preguntas de investigación. "
    "Simula el comportamiento de un agente investigador para proporcionar respuestas detalladas y precisas."
)

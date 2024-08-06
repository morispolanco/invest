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
        "max_tokens": 2000,
        "temperature": 0,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["\""],
        "stream": True
    }
    
    response = requests.post(url, headers=headers, json=data, stream=True)
    if response.status_code == 200:
        resultado = ""
        for chunk in response.iter_content(1024):
            resultado += chunk.decode("utf-8")
        try:
            json_data = json.loads(resultado)
            return json_data['choices'][0]['message']['content']
        except json.JSONDecodeError:
            return "Error: unable to parse JSON response"
    else:
        return f"Error: {response.status_code} - {response.text}"

# Entrada del usuario
consulta_usuario = st.text_input("Ingrese su pregunta de investigación:")

if consulta_usuario:
    if st.button("Investigar"):
        with st.spinner("Investigando..."):
            resultado = llamar_api_together(f"Actúa como un investigador y investiga la siguiente pregunta: {consulta_usuario}")
            st.write("Resultados de la investigación:")
            st.write(resultado)

# Barra lateral con información sobre la app
st.sidebar.header("Acerca de esta aplicación")
st.sidebar.info(
    "Esta aplicación utiliza la API de Together para investigar y responder a preguntas de investigación. "
    "Simula el comportamiento de un agente investigador para proporcionar respuestas detalladas y precisas."
)

import streamlit as st
import requests

# Título de la aplicación en Streamlit
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
        "max_tokens": 912,
        "temperature": 0,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": [""],
        "stream": False  # Cambiado a False para simplicidad
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Entrada del usuario
consulta_usuario = st.text_input("Ingrese su pregunta de investigación:")

if consulta_usuario and st.button("Investigar"):
    with st.spinner("Investigando..."):
        resultado = llamar_api_together(f"Actúa como un investigador y realiza una investigación sobre la siguiente pregunta: {consulta_usuario}")
        st.write("Resultados de la investigación:")
        st.write(resultado)

# Instrucciones para configurar el secreto
st.sidebar.header("Instrucciones de Configuración")
st.sidebar.info(
    "Para usar esta aplicación, necesita configurar su clave API de Together en los secretos de Streamlit. "
    "Cree un archivo llamado `.streamlit/secrets.toml` en el directorio raíz de su aplicación y agregue la siguiente línea:\n\n"
    "TOGETHER_API_KEY = 'su_clave_api_aquí'\n\n"
    "Reemplace 'su_clave_api_aquí' con su clave API de Together."
)

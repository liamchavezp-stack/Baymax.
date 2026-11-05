import streamlit as st
from openai import OpenAI
from gtts import gTTS
import io

st.set_page_config(
    page_title="Baymax - Tutor de Filosofía", 
    page_icon="🤖", 
    layout="centered", 
    initial_sidebar_state="collapsed", 
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# Estilo visual plateado / gris metálico con detalles en azul suave
css_plateado = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;} .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;} [data-testid="stStatusWidget"] {display: none;}
    
    .stApp {
        background: linear-gradient(135deg, #e0e5ec 0%, #cbd5e1 50%, #94a3b8 100%); 
        max-width: 100%; 
        padding: 0; 
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        font-family: 'Inter', sans-serif !important; 
        color: #1e293b !important; 
        text-align: center; 
        font-size: 2.2rem !important; 
        font-weight: 700 !important; 
        text-shadow: 0 1px 2px rgba(255,255,255,0.8); 
        padding-top: 1.5rem !important; 
        margin-bottom: 0.1rem !important;
    }
    
    .stCaption {
        text-align: center; 
        color: #475569 !important; 
        font-family: 'Inter', sans-serif !important; 
        font-size: 0.95rem !important; 
        margin-bottom: 1.2rem !important;
    }
    
    [data-testid="stChatMessage"] {
        border-radius: 18px; 
        padding: 1rem 1.2rem !important; 
        margin: 0.5rem 0 !important;
    }
    
    /* Mensaje de Baymax (Asistente) */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%) !important; 
        border: 1px solid rgba(148,163,184,0.3) !important; 
        border-left: 4px solid #3b82f6 !important; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Mensaje del Usuario */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;

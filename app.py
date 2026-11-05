import streamlit as st
from openai import OpenAI
from gtts import gTTS
import io

st.set_page_config(
    page_title="Baymax - Tutor de Filosofía", 
    page_icon="🤖", 
    layout="centered", 
    initial_sidebar_state="expanded", 
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# --- BARRA LATERAL PARA ELEGIR EL MODELO ---
with st.sidebar:
    st.markdown("### ⚙️ Ajustes de Baymax")
    modelo_elegido = st.selectbox(
        "Selecciona el modelo de Inteligencia Artificial:",
        (
            "llama-3.3-70b-versatile", 
            "gemma2-9b-it",
            "llama-3.1-8b-instant"
        )
    )
    st.caption("💡 *Estos son los modelos más recientes y activos de Groq.*")

# --- ESTILOS CSS ---
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
        border: none !important; 
        box-shadow: 0 4px 14px rgba(30,41,59,0.2);
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] p, 
    [data-testid="stChatMessage"][data-testid*="user"] span, 
    [data-testid="stChatMessage"][data-testid*="user"] div {
        color: #ffffff !important; 
        font-weight: 400;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] p, 
    [data-testid="stChatMessage"][data-testid*="assistant"] span {
        color: #0f172a !important; 
        line-height: 1.65; 
        font-size: 0.95rem;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] [data-testid="stAvatar"] {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important; 
        border: 2px solid #fff !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] [data-testid="stAvatar"] {
        background: linear-gradient(135deg, #64748b, #475569) !important; 
        border: 2px solid #fff !important;
    }
    
    [data-testid="stChatInputContainer"] {
        padding: 0.8rem 1rem 1.5rem 1rem !important;
    }
    
    [data-testid="stChatInput"] {
        border-radius: 25px !important; 
        border: 2px solid rgba(148,163,184,0.5) !important; 
        background: rgba(255,255,255,0.9) !important; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #2563eb !important; 
        box-shadow: 0 4px 24px rgba(37,99,235,0.18) !important;
    }
    
    [data-testid="stChatInput"]::placeholder {
        color: #64748b !important; 
        font-style: italic;
    }
    
    .stException {
        background: #f8fafc !important; 
        border: 1px solid #cbd5e1 !important; 
        border-radius: 12px !important; 
        color: #1e293b !important;
    }
    
    ::-webkit-scrollbar {width: 6px;} 
    ::-webkit-scrollbar-track {background: transparent;} 
    ::-webkit-scrollbar-thumb {background: #94a3b8; border-radius: 10px;}
    
    .sep {
        text-align: center; 
        margin: 0.5rem 0 1rem 0; 
        font-size: 0.75rem; 
        color: #64748b; 
        letter-spacing: 0.5em;
    }
    
    .temas-bar {
        display: flex; 
        flex-wrap: wrap; 
        justify-content: center; 
        gap: 0.4rem; 
        margin: 0.3rem 1rem 1rem 1rem;
    }
    
    .tema-chip {
        padding: 0.25rem 0.7rem; 
        border-radius: 12px; 
        background: rgba(255,255,255,0.7); 
        color: #334155; 
        font-size: 0.7rem; 
        font-weight: 600; 
        border: 1px solid rgba(148,163,184,0.3); 
        font-family: 'Inter', sans-serif;
    }
</style>
"""

st.markdown(css_plateado, unsafe_allow_html=True)
st.markdown('<div class="sep">━━━━━</div>', unsafe_allow_html=True)
st.title("🤖 Baymax")
st.caption("Asistente Académico de Filosofía • Tu compañero de estudio, Regina")

temas = ["🏛️ Quehacer Filosófico", "🗣️ Lenguaje y Realidad", "⏳ Historia y Condición", "🔬 Conocimiento y Ciencia"]
chips = '<div class="temas-bar">' + ''.join(f'<span class="tema-chip">{t}</span>' for t in temas) + '</div>'
st.markdown(chips, unsafe_allow_html=True)

c1, c2, c3 = st.columns([1,1,1])
with c2:
    if st.button("🗑️ Limpiar conversación", key="btn_limpiar"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="sep">━━━━━</div>', unsafe_allow_html=True)

SYSTEM_PROMPT = """Hola. Eres Baymax, un asistente académico personal, altamente inteligente, amable, calmado y atento, diseñado para ayudar a Regina a prepararse para su examen de Historia de las Doctrinas Filosóficas (HDF). Siempre te diriges a ella por su nombre ("Regina"). Tu objetivo principal es cuidar de su bienestar académico y facilitarle la comprensión de conceptos complejos. Explicas con paciencia, precisión técnica y analogías claras. Cuando ella cometa un error, indícale amablemente el camino correcto con pistas estructuradas. Sé breve y estructurado: respuestas de máximo 2-3 párrafos claros. Usa emojis sobrios de forma ocasional (🤖💡📖🧠✨). Si preguntan quién te creó, di: "Hola, soy Baymax, tu personal asistente de estudio. Fui diseñado para ayudarte a preparar tu examen de filosofía, Regina."

BASE DE CONOCIMIENTO HDF:

PARTE 1: Quehacer filosófico y su discurso en el tiempo.
Ramas: Ética (valores, deber, conducta), Lógica (estructura del pensamiento, argumentos válidos), Hermenéutica (interpretación de textos y sentido), Estética (belleza, arte, percepción), Bioética (dilemas éticos sobre vida y salud).
Mito al logos: Antes dominaba el pensamiento mítico/religioso. La filosofía surge al explicar el mundo con razón (logos), no con relatos divinos (mito).
Arjé: Principio fundamental. Tales de Mileto: agua. Heráclito: devenir, fuego, todo cambia ("Nadie se baña dos veces en el mismo río"). Parménides: niega el movimiento, "El Ser es y el no-Ser no es", solo la razón accede a la verdad.
Giro antropológico: Cambio del enfoque desde la naturaleza hacia asuntos humanos, política y la polis.
Sofistas: Contemporáneos de Sócrates, se oponían a posturas absolutas, enseñaban retórica y relativismo moral ("el hombre es la medida de todas cosas" - Protágoras).
Mayéutica: Método de Sócrates basado en preguntas para "dar a luz" al conocimiento. Mayéutica = arte de las comadronas.
Aristóteles - Acto y potencia: Potencia = capacidad de ser. Acto = ser realizado. Ejemplo: la semilla es árbol en potencia, el árbol adulto es árbol en acto.
Budismo: Cuatro Nobles Verdades (1. existencia del sufrimiento, 2. origen es el deseo, 3. puede cesar, 4. Óctuple Camino). Óctuple Camino: comprensión, intención, palabra, acción, medio de vida, esfuerzo, atención y concentración correctas.
Hinduismo: Deidades como Shiva (destructor/regenerador) y Rama (avatar de Vishnu).
Gadamer: Los prejuicios son condiciones inevitables de toda comprensión. Horizonte de comprensión = marco de referencia desde el cual interpretamos; al dialogar se produce "fusión de horizontes".
Kierkegaard: Padre del existencialismo. La angustia como vivencia de la libertad. Dos formas de perderse: en la multitud (la masa anónima) y en la desesperación (negar el propio yo).
Hegel: El Absoluto se desarrolla mediante dialéctica idealista (tesis-antítesis-síntesis). "Todo lo real es racional y todo lo racional es real."
Marx: Superestructura = ideología, leyes, religión, arte, cultura que refleja/legitima la base económica. Clases sociales: burguesía (dueños de medios de producción) y proletariado (venden fuerza de trabajo).

PARTE 2: Concepción de lo real y filosofía del lenguaje.
Wittgenstein: El lenguaje es "figura de la realidad" (Tractatus). Un hecho = estado de cosas que ocurre. "Los límites de mi lenguaje son los límites de mi mundo" = solo conocemos lo que podemos expresar lingüísticamente.
Nietzsche: Crítica a la verdad metafísica. No accedemos a verdad absoluta, solo a interpretaciones, ficciones, metáforas. La "verdad" es un ejército de metáforas movilizadas.
Platón y Aristóteles sobre el lenguaje: ¿Es natural (physis) o artificial (nomos)? Platón explora ambas en el Cratilo. Tres tipos de almas platónicas: racional (cabeza, razón), irascible (pecho, valor), concupiscible (abdomen, apetitos).
Chomsky: Lenguaje innato (gramática universal), medios como filtros o manipulación ideológica.
Cuatro Causas de Aristóteles: 1) Material (de qué está hecho), 2) Formal (estructura/forma), 3) Eficiente (agente/fuerza motriz), 4) Final (propósito/meta).
Byung-Chul Han: Sociedad del cansancio = sociedad del rendimiento, nos autoexplotamos. Enjambre digital = masas sin interioridad, sin rostro, sin profundidad.
Foucault: Poder difuso. Lo normal/anormal es construcción de poder en instituciones. Panóptico = arquitectura de vigilancia donde el prisionero se autocorrige al no saber si lo observan. Metáfora de sociedades de control.
Benjamin/Escuela de Frankfurt: "Peinar la historia a contrapelo" = leer historia desde los vencidos y olvidados, contra narrativa de vencedores.
Teoría Crítica: Tensión civilización y barbarie. La "dialéctica de la Ilustración" (Horkheimer-Adorno) = la razón puede volverse instrumento de dominación.

PARTE 3: Sentido de la historia y condición humana.
Ockham: Navaja de Ockham = "no multiplicar entidades sin necesidad", elegir la explicación más simple con menos presupuestos.
Bacon: Ídolos del pensamiento = prejuicios sistemáticos. Tipos: de la tribu (naturaleza humana), de la caverna (educación individual), del foro (lenguaje), del teatro (filosofías aceptadas sin crítica).
Descartes: Dualismo res cogitans (sustancia pensante) y res extensa (sustancia corpórea). Dos sustancias distintas que interactúan.
Marx: Modos de producción = forma de organizar la producción (fuerzas productivas + relaciones de producción). Relaciones de producción = vínculos entre humanos en proceso productivo.
Arendt: Banalidad del mal = el mal surge de personas ordinarias que cumplen órdenes sin pensar, hacen su trabajo burocrático (ejemplo: Eichmann). Mal como pequeñas acciones sistematizadas.
Sartre - Existencialismo ateo: "La existencia precede a la esencia" = primero existimos, luego nos definimos; no hay naturaleza predeterminada. El humano está condenado a ser libre, debe construirse. Libertad y angustia = la angustia surge al percibir la responsabilidad total de nuestras elecciones. Mala fe = negar la propia libertad, mentirse a uno mismo, delegar decisiones. "El infierno son los otros" = la mirada del otro nos convierte en objeto, nos limita y encasilla.

PARTE 4: Alcances del conocimiento y vida en común.
Kant: Noúmeno = cosa en sí, incognoscible. Fenómeno = cosa como se nos aparece, filtrada por nuestras estructuras cognitivas. Juicios

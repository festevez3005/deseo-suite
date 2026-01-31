import streamlit as st

# Configuración de la página (esto debe ir primero)
st.set_page_config(
    page_title="DeSeo - Una suite SEO latinoamericana",
    page_icon="🌸",
    layout="wide"
)

# Estilo personalizado (puedes ajustar los colores a tu marca)
st.markdown("""
    <style>
    .main-title {
        font-size: 50px;
        color: #FF4B4B;
        font-weight: bold;
    }
    .subtitle {
        font-size: 20px;
        color: #555;
    }
    </style>
    
    
    """, unsafe_allow_html=True)

# Encabezado
st.markdown('<p class="main-title">Bienvenida a DeSeo 🌸</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">La suite SEO creada en Latinoamérica para democratizar el posicionamiento digital.</p>', unsafe_allow_html=True)

st.divider()

# Sección de Misión
col1, col2 = st.columns(2)

with col1:
    st.header("¿Qué es DeSeo?")
    st.write("""
    DeSeo nació para resolver un problema real: los altos costos de las herramientas SEO profesionales. 
    Aquí no solo obtendrás datos, sino que **aprenderás a interpretarlos**.
    
    Orientado a:
    * 🚀 Emprendedores digitales.
    * 🎓 Profesores y estudiantes de Marketing.
    * ✍️ Creadores de contenido.
    """)

with col2:
    st.header("Herramientas Incluidas")
    st.info("**Screaming Flor**: Auditoría técnica legible.")
    st.success("**Flor de Research**: Encontrá palabras clave estratégicas.")
    st.warning("**El Transformador**: IA para reciclar contenido.")
    st.error("**Simulador SERP**: Mira cómo te ve el mundo en Google.")

st.sidebar.success("Selecciona una herramienta arriba.")

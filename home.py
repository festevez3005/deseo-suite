import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="DeSeo - Una herramienta de SEO con corazón argentino",
    page_icon="🌸",
    layout="wide"
)

# Estilo personalizado
st.markdown("""
    <style>
    .main-title {
        font-size: 45px;
        color: #FF4B4B;
        font-weight: bold;
        text-align: center;
    }
    .manifesto-box {
        background-color: #f9f9f9;
        padding: 30px;
        border-left: 5px solid #FF4B4B;
        border-radius: 10px;
        margin: 20px 0;
        font-style: italic;
    }
    .highlight {
        color: #FF4B4B;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.markdown('<p class="main-title">Bienvenida a DeSeo 🌸</p>', unsafe_allow_html=True)

# --- TU REFLEXIÓN (MANIFIESTO) ---
st.markdown("""
    <div class="manifesto-box">
        <h3>✨ Una reflexión antes de empezar...</h3>
        <p>
            Los datos deben ser siempre analizados en su <b>contexto</b>. Revisarlos no implica que vayamos a tener certezas absolutas; 
            trabajamos con humanos, cuyos comportamientos no siempre son predecibles. 
        </p>
        <p>
            Una buena estrategia de SEO contempla esto: está contextualizada y acompaña los comportamientos. 
            A diferencia de otros canales, el SEO nos da el <span class="highlight">poder sobre el mensaje y sobre el canal</span>. 
            Aunque estemos mediados por un algoritmo o una IA, podemos interactuar con las personas de manera más directa.
        </p>
        <p>
            Recordemos que las personas <b>no son solo "buyer personas" ni audiencias segmentadas</b>. 
            Las tendencias no determinan el futuro, porque si así fuera, no pensaríamos que los seres humanos podemos cambiar.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Sección de Herramientas
st.subheader("🛠️ Tu Suite de Trabajo")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 🌸 Screaming Flor\nAuditoría técnica y diagnósticos legibles.")

with col2:
    st.success("### 🔍 Flor de Research\nKeyword research geolocalizado con IA.")

with col3:
    st.warning("### ✍️ El Transformador\n(Próximamente) Reciclaje de contenido optimizado.")

st.sidebar.markdown("---")
st.sidebar.write("Hecho con ❤️ en Latam")

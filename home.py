import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="DeSeo - Suite SEO Latinoamericana",
    page_icon="🌸",
    layout="wide"
)

# ESTILO CORREGIDO PARA ALTO CONTRASTE
st.markdown("""
    <style>
    .main-title {
        font-size: 45px;
        color: #FF4B4B;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    .manifesto-box {
        background-color: #1E1E1E; /* Fondo oscuro sólido */
        padding: 35px;
        border-left: 6px solid #FF4B4B;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .manifesto-box h3 {
        color: #FF4B4B !important;
        margin-bottom: 20px;
    }
    .manifesto-text {
        color: #E0E0E0 !important; /* Texto gris muy claro/blanco */
        font-size: 18px;
        line-height: 1.6;
        font-style: italic;
    }
    .highlight {
        color: #FF4B4B;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.markdown('<p class="main-title">Bienvenida a DeSeo 🌸</p>', unsafe_allow_html=True)

# --- MANIFIESTO CON CONTRASTE CORREGIDO ---
st.markdown("""
    <div class="manifesto-box">
        <h3>✨ Una reflexión antes de empezar...</h3>
        <p class="manifesto-text">
            Los datos deben ser siempre analizados en su <b>contexto</b>. Revisarlos no implica que vayamos a tener certezas absolutas; 
            trabajamos con humanos, cuyos comportamientos no siempre son predecibles. 
            <br><br>
            Una buena estrategia de SEO contempla esto: está contextualizada y acompaña los comportamientos. 
            A diferencia de otros canales, el SEO nos da el <span class="highlight">poder sobre el mensaje y sobre el canal</span>. 
            Aunque estemos mediados por un algoritmo o una IA, podemos interactuar con las personas de manera más directa.
            <br><br>
            Recordemos que las personas <b>no son solo "buyer personas" ni audiencias segmentadas</b>. 
            Las tendencias no determinan el futuro, porque si así fuera, no pensaríamos que los seres humanos podemos cambiar.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Sección de Herramientas (Cards simples de Streamlit)
st.subheader("🛠️ Tu Suite de Trabajo")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 🌸 Screaming Flor\nAuditoría técnica y diagnósticos legibles.")

with col2:
    st.success("### 🔍 Flor de Research\nKeyword research geolocalizado con IA.")

with col3:
    st.warning("### ✍️ El Transformador\nOptimización y reciclaje de contenidos.")

st.sidebar.markdown("---")
st.sidebar.write("Hecho con ❤️ en Latam")

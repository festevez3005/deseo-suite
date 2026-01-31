import streamlit as st

st.set_page_config(
    page_title="DeSeo - Suite SEO Latinoamericana",
    page_icon="🌸",
    layout="wide"
)

# Estilo corregido para visibilidad en temas oscuros/claros
st.markdown("""
    <style>
    .main-title {
        font-size: 45px;
        color: #FF4B4B;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .manifesto-box {
        background-color: #1E1E1E; /* Fondo oscuro para contraste */
        padding: 40px;
        border-radius: 15px;
        border: 1px solid #333;
        margin: 20px 0;
        color: #FFFFFF; /* Texto blanco */
        line-height: 1.6;
    }
    .highlight {
        color: #FF4B4B;
        font-weight: bold;
    }
    .concept-tag {
        background-color: #333;
        padding: 4px 10px;
        border-radius: 5px;
        font-family: monospace;
        color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">Bienvenida a DeSeo 🌸</p>', unsafe_allow_html=True)

# --- NUEVO MANIFIESTO: INGENIERÍA INVERSA Y SOBERANÍA ---
st.markdown("""
    <div class="manifesto-box">
        <h2 style='color: #FF4B4B; text-align: center;'>Soberanía Digital e Ingeniería Inversa</h2>
        <p>
            <b>DeSeo</b> no nació solo como una suite de herramientas, sino como un acto de resistencia para 
            <span class="highlight">democratizar el posicionamiento digital</span> en nuestra región.
        </p>
        <p>
            Nos guiamos por el principio de la <span class="concept-tag">Ingeniería Inversa</span>: 
            creemos que entender las entrañas de cómo funcionan los algoritmos y los motores de búsqueda nos otorga 
            la capacidad real de actuar sobre ellos. No se trata de seguir reglas a ciegas, sino de descifrar la lógica 
            para jugar nuestro propio juego.
        </p>
        <p>
            Buscamos la <span class="concept-tag">Soberanía Digital</span>. En un mundo mediado por cajas negras y 
            algoritmos opacos, recuperar el conocimiento es recuperar la autonomía. Entender cómo funciona la 
            tecnología es el primer paso para no ser solo usuarios, sino dueños de nuestro mensaje y nuestro canal.
        </p>
        <hr style="border: 0.1px solid #444;">
        <p style="font-style: italic; text-align: center; color: #BBB;">
            "Revisar datos no es buscar certezas, es acompañar el comportamiento humano. Las personas no son audiencias 
            segmentadas; son voluntades que cambian, y el SEO es nuestra forma de dialogar con ellas."
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Sección de Herramientas
st.subheader("🛠️ Tu Suite de Soberanía Digital")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 🌸 Screaming Flor\nAuditoría técnica para desarmar la estructura de cualquier web.")

with col2:
    st.success("### 🔍 Flor de Research\nKeyword research para entender qué busca y desea la gente.")

with col3:
    st.warning("### ✍️ El Transformador\nInteligencia aplicada para potenciar tu mensaje original.")

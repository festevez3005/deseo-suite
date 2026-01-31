import streamlit as st
import pandas as pd
from seo_logic import get_google_suggestions, analyze_keywords_with_openai, get_research_glossary

st.set_page_config(page_title="Flor de Research - DeSeo", layout="wide")

st.title("🔍 Flor de Research")
st.markdown("Descubre qué busca tu audiencia y cómo responder a sus necesidades.")

# --- SECCIÓN EDUCATIVA ---
with st.expander("🎓 ¿Qué es el Keyword Research?"):
    st.write("""
    El Keyword Research es la base de cualquier estrategia digital. No se trata solo de encontrar palabras con mucho tráfico, 
    sino de entender **la intención** detrás de ellas.
    """)
    glossary = get_research_glossary()
    for term, desc in glossary.items():
        st.markdown(f"**{term}:** {desc}")

st.divider()

# --- CONFIGURACIÓN ---
with st.sidebar:
    st.header("Configuración de IA")
    # Intentamos obtener la key de los secretos o pedimos entrada manual
    api_key_input = st.text_input("OpenAI API Key", type="password", 
                                 help="Tu key se usa solo para esta sesión y no se guarda.")
    # Priorizar la key de st.secrets si existe
    api_key = st.secrets.get("OPENAI_API_KEY") or api_key_input

st.subheader("1. Generador de Ideas")
col1, col2 = st.columns([2, 1])

with col1:
    seed = st.text_input("Introduce una palabra base (ej: marketing digital)", placeholder="zapatos de cuero")

if seed:
    suggestions = get_google_suggestions(seed)
    
    if suggestions:
        st.success(f"Encontramos {len(suggestions)} sugerencias basadas en búsquedas reales.")
        
        # Mostrar sugerencias crudas
        with st.expander("Ver sugerencias de autocompletado"):
            st.write(", ".join(suggestions))
        
        st.divider()
        st.subheader("2. Análisis Estratégico con IA")
        
        if not api_key:
            st.info("💡 Para clasificar estas palabras por intención y etapa del embudo, por favor introduce tu OpenAI API Key en la barra lateral.")
        else:
            if st.button("✨ Analizar Keywords con DeSeo IA"):
                with st.spinner("La IA está clasificando y generando ideas de contenido..."):
                    analysis = analyze_keywords_with_openai(api_key, seed, suggestions)
                    
                    if "error" in analysis:
                        st.error(f"Error con la API de OpenAI: {analysis['error']}")
                    else:
                        # Extraer la lista del JSON (OpenAI suele devolver una lista bajo una llave)
                        key_list = list(analysis.values())[0]
                        df_keywords = pd.DataFrame(key_list)
                        
                        st.balloons()
                        st.dataframe(df_keywords, use_container_width=True)
                        
                        # Opción de descarga
                        csv = df_keywords.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Descargar Estrategia", data=csv, file_name=f"research_{seed}.csv")
    else:
        st.warning("No pudimos obtener sugerencias para esa palabra. Intenta con un término más general.")

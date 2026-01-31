import streamlit as st
import pandas as pd
from seo_logic import (
    get_latam_countries, get_expanded_suggestions, 
    analyze_keywords_with_openai, get_research_glossary
)

st.set_page_config(page_title="Flor de Research - DeSeo", layout="wide")

st.title("🔍 Flor de Research")
st.markdown("Geolocaliza tu estrategia y entiende la mente de tu usuario.")

# --- GLOSARIO EDUCATIVO ---
with st.expander("📚 Conceptos Clave de Keyword Research"):
    glosario = get_research_glossary()
    cols = st.columns(2)
    for i, (k, v) in enumerate(glosario.items()):
        cols[i%2].write(f"**{k}:** {v}")

st.divider()

# --- CONFIGURACIÓN ---
with st.sidebar:
    st.header("Ajustes de Búsqueda")
    paises = get_latam_countries()
    pais_sel = st.selectbox("Selecciona País", list(paises.keys()))
    
    st.header("IA Estratega")
    api_key_input = st.text_input("OpenAI API Key", type="password")
    api_key = st.secrets.get("OPENAI_API_KEY") or api_key_input

# --- ENTRADA ---
col_in, col_btn = st.columns([3, 1])
with col_in:
    seed = st.text_input("Palabra semilla o Nicho", placeholder="ej: cursos de cocina")

if st.button("🚀 Investigar Mercado", type="primary") and seed:
    with st.status("Rastreando sugerencias locales y analizando con IA...", expanded=True) as status:
        
        # 1. Scraping de Google (Gratis y Legal)
        keywords_raw = get_expanded_suggestions(seed, paises[pais_sel])
        
        if keywords_raw:
            st.write(f"✅ Se encontraron {len(keywords_raw)} variaciones reales en {pais_sel}.")
            
            if not api_key:
                status.update(label="Análisis básico completo (Sin IA)", state="complete")
                st.warning("Añade tu API Key para desbloquear la intención de búsqueda y pistas educativas.")
                st.write(pd.DataFrame(keywords_raw, columns=["Keywords Sugeridas"]))
            else:
                # 2. Análisis con IA
                st.write("🧠 La IA está clasificando por intención y creando pistas...")
                analysis = analyze_keywords_with_openai(api_key, seed, keywords_raw, pais_sel)
                
                if "error" in analysis:
                    st.error(f"Error en IA: {analysis['error']}")
                else:
                    df = pd.DataFrame(analysis['keywords'])
                    status.update(label="¡Estrategia Lista!", state="complete")
                    
                    # --- RESULTADOS ---
                    st.balloons()
                    
                    # KPIs Rápidos
                    c1, c2 = st.columns(2)
                    with c1:
                        trans = len(df[df['intencion'] == 'Transaccional'])
                        st.metric("Oportunidades de Venta", f"{trans} keywords")
                    with c2:
                        inf = len(df[df['intencion'] == 'Informativa'])
                        st.metric("Oportunidades de Contenido", f"{inf} keywords")

                    # Tabla Maestra
                    st.subheader(f"📊 Plan de Keywords para {pais_sel}")
                    st.dataframe(df, use_container_width=True)
                    
                    # Exportación
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Descargar Estrategia", data=csv, file_name=f"research_{seed}_{pais_sel}.csv")
        else:
            st.error("No se pudieron obtener datos. Intenta con una palabra más simple.")

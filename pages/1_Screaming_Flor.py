import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from seo_logic import audit_one, load_sitemap_urls, to_csv_bytes, get_glossary

st.set_page_config(page_title="DeSeo - Screaming Flor", layout="wide")

st.title("🌸 Screaming Flor: Auditoría Pro")

# --- SECCIÓN: GLOSARIO ---
with st.expander("📖 Glosario: Entiende tus resultados"):
    glossary = get_glossary()
    cols = st.columns(2)
    for i, (term, desc) in enumerate(glossary.items()):
        cols[i % 2].markdown(f"**{term}**: {desc}")

# --- CONFIGURACIÓN ---
st.sidebar.header("Opciones de Auditoría")
mode = st.sidebar.radio("Fuente", ["Sitemap XML", "Lista Manual"])
max_pages = st.sidebar.slider("Límite de páginas", 10, 100, 50)

urls = []
if mode == "Sitemap XML":
    s_url = st.text_input("URL del Sitemap", placeholder="https://tusitio.com/sitemap.xml")
    if s_url: urls = load_sitemap_urls(s_url, max_pages)
else:
    t_area = st.text_area("Pega tus URLs")
    if t_area: urls = [u.strip() for u in t_area.splitlines() if u.strip()][:max_pages]

if st.button("🚀 Ejecutar Análisis Masivo", type="primary") and urls:
    results = []
    progress = st.progress(0)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(audit_one, u): u for u in urls}
        for i, fut in enumerate(as_completed(futures)):
            results.append(fut.result())
            progress.progress((i + 1) / len(urls))

    df = pd.DataFrame(results)
    
    # --- VISUALIZACIÓN DE RESULTADOS ---
    st.divider()
    
    # 1. Gráficos de resumen
    st.subheader("📊 Resumen del Sitio")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.write("**Distribución por Tipo de Recurso**")
        st.bar_chart(df['tipo'].value_counts())
        
    with col_chart2:
        st.write("**Salud del Sitio (SEO Score)**")
        # Filtrar solo los que tienen score numérico
        scores = df[df['seo_score'] != "N/A"]['seo_score']
        if not scores.empty:
            st.line_chart(scores)

    # 2. Tabla de Datos
    st.subheader("📋 Detalle Técnico")
    # Limpiamos la tabla para que sea legible
    display_df = df[['url', 'tipo', 'status_code', 'seo_score', 'response_time', 'h1_count']]
    st.dataframe(display_df.style.background_gradient(subset=['response_time'], cmap='YlOrRd'), use_container_width=True)

    st.download_button("📥 Descargar Reporte CSV", data=to_csv_bytes(df), file_name="auditoria_deseo_completa.csv")

elif not urls:
    st.info("Configura la fuente en la izquierda y pulsa el botón para comenzar.")

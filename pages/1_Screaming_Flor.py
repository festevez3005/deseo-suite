import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from seo_logic import audit_one, load_sitemap_urls, to_csv_bytes, get_glossary

st.set_page_config(page_title="Screaming Flor - Auditoría Pro", layout="wide")

st.title("🌸 Screaming Flor: Auditoría de Sitio")

# --- GLOSARIO ---
with st.expander("📖 Glosario de Conceptos SEO"):
    glossary = get_glossary()
    cols = st.columns(3)
    for i, (term, definition) in enumerate(glossary.items()):
        cols[i % 3].markdown(f"**{term}:** {definition}")

# --- CONFIGURACIÓN ---
st.sidebar.header("Panel de Control")
mode = st.sidebar.radio("Fuente", ["Sitemap XML", "Lista Manual"])
max_pages = st.sidebar.slider("Límite de páginas", 10, 100, 50)

urls = []
if mode == "Sitemap XML":
    s_url = st.text_input("URL del Sitemap", placeholder="https://tusitio.com/sitemap.xml")
    if s_url: urls = load_sitemap_urls(s_url, max_pages)
else:
    t_area = st.text_area("URLs (una por línea)")
    if t_area: urls = [u.strip() for u in t_area.splitlines() if u.strip()][:max_pages]

# --- EJECUCIÓN ---
if st.button("🚀 Ejecutar Auditoría", type="primary") and urls:
    with st.status("Analizando sitio...", expanded=True) as status:
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(audit_one, u): u for u in urls}
            for i, fut in enumerate(as_completed(futures)):
                results.append(fut.result())
        status.update(label="¡Análisis Finalizado!", state="complete", expanded=False)

    df = pd.DataFrame(results)

    # --- RESUMEN ---
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Salud Promedio", f"{int(df['seo_score'].mean())}/100")
    c2.metric("Páginas con Schema", f"{len(df[df['schema_detected'] != 'No'])}")
    c3.metric("Promedio Títulos", f"{int(df['title_len'].mean())} car.")
    c4.metric("Sin Meta Desc.", f"{len(df[df['meta_desc'] == ''])}")

    # --- TABLA ESTILO SCREAMING FROG ---
    st.subheader("📊 Tabla de Datos Detallada")
    
    # Definimos las columnas y su orden
    cols_to_show = [
        'url', 'seo_score', 'status_code', 'title', 'title_len', 
        'meta_desc', 'meta_desc_len', 'h1_count', 'schema_detected', 'internal_links'
    ]
    
    def color_score(v):
        if not isinstance(v, (int, float)): return ''
        if v < 60: return 'background-color: #d9534f; color: white;'
        if v < 90: return 'background-color: #f0ad4e; color: black;'
        return 'background-color: #5cb85c; color: white;'

    # Mostramos la tabla. Streamlit permite expandir las celdas de texto automáticamente.
    st.dataframe(
        df[cols_to_show].style.applymap(color_score, subset=['seo_score']), 
        use_container_width=True
    )

    # --- EXPORTACIÓN ---
    st.download_button("📥 Descargar Reporte CSV", data=to_csv_bytes(df), file_name="auditoria_deseo.csv")

elif not urls and 's_url' in locals():
    st.info("Configura la fuente en el panel lateral para comenzar.")

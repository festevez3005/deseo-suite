import streamlit as st
import pandas as pd
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
# IMPORTANTE: Aquí traemos la lógica del otro archivo
from seo_logic import load_sitemap_urls, audit_one, add_issue_flags, normalize_url, to_csv_bytes

st.set_page_config(page_title="Screaming Flor", layout="wide")

st.title("🌸 Screaming Flor")
st.markdown("Auditoría técnica enfocada en prioridades.")

# --- SIDEBAR ---
with st.sidebar:
    mode = st.radio("Fuente:", ["Sitemap", "Manual"])
    max_urls = st.slider("Máximo de URLs", 10, 100, 50)

# --- CARGA DE URLS ---
urls = []
if mode == "Sitemap":
    s_url = st.text_input("URL del Sitemap")
    if s_url: urls = load_sitemap_urls(s_url, max_urls)
else:
    t_area = st.text_area("Pega URLs")
    if t_area: urls = [normalize_url(u) for u in t_area.splitlines() if u][:max_urls]

# --- EJECUCIÓN ---
if st.button("🚀 Iniciar Auditoría", type="primary") and urls:
    results = []
    progress = st.progress(0)
    
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(audit_one, u): u for u in urls}
        for i, fut in enumerate(as_completed(futures)):
            results.append(fut.result())
            progress.progress((i + 1) / len(urls))
    
    df = pd.DataFrame(results)
    df = add_issue_flags(df)

    # --- TABS PEDAGÓGICOS ---
    tab1, tab2 = st.tabs(["🎯 Prioridades", "📊 Datos"])
    with tab1:
        st.write("Aquí verás los errores críticos primero.")
        st.dataframe(df) # Aquí puedes filtrar por severidad
    with tab2:
        st.download_button("Descargar Reporte", data=to_csv_bytes(df), file_name="audit.csv")

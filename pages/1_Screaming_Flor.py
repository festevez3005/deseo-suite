import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from seo_logic import audit_one, load_sitemap_urls, to_csv_bytes, get_glossary

st.set_page_config(page_title="Screaming Flor - Auditoría Pro", layout="wide")

st.title("🌸 Screaming Flor: Auditoría de Sitio")

# --- GLOSARIO ---
with st.expander("📖 Glosario de Conceptos SEO"):
    glossary = get_glossary()
    cols = st.columns(2)
    for i, (term, definition) in enumerate(glossary.items()):
        cols[i % 2].markdown(f"**{term}:** {definition}")

# --- CONFIGURACIÓN ---
st.sidebar.header("Panel de Control")
mode = st.sidebar.radio("Fuente de URLs", ["Sitemap XML", "Lista Manual"])
max_pages = st.sidebar.slider("Límite de páginas", 10, 100, 50)

urls = []
if mode == "Sitemap XML":
    s_url = st.text_input("Ingresa la URL del Sitemap")
    if s_url: urls = load_sitemap_urls(s_url, max_pages)
else:
    t_area = st.text_area("Pega tus URLs (una por línea)")
    if t_area: urls = [u.strip() for u in t_area.splitlines() if u.strip()][:max_pages]

# --- EJECUCIÓN ---
if st.button("🚀 Iniciar Auditoría Masiva", type="primary") and urls:
    with st.status("Analizando sitio...", expanded=True) as status:
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(audit_one, u): u for u in urls}
            for i, fut in enumerate(as_completed(futures)):
                results.append(fut.result())
        status.update(label="¡Análisis Finalizado!", state="complete", expanded=False)

    df = pd.DataFrame(results)

    # --- 1. SECCIÓN DE ALERTAS ---
    all_issues = [issue for sublist in df['critical_issues'] for issue in sublist]
    if all_issues:
        st.subheader("🚨 Hallazgos Críticos")
        issue_series = pd.Series(all_issues).value_counts()
        for issue, count in issue_series.items():
            st.error(f"**{issue}:** Encontrado en {count} páginas.")

    # --- 2. RESUMEN ESTRATÉGICO ---
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Salud Promedio", f"{int(df['seo_score'].mean())}/100")
    
    con_schema = len(df[df['schema_detected'] != "No"])
    c2.metric("Páginas con Schema", f"{con_schema}")
    
    avg_links = df[df['content_type'] == 'HTML']['internal_links'].mean()
    c3.metric("Promedio Enlaces Int.", f"{avg_links:.1f}")

    # --- 3. TABLA DETALLADA ---
    st.subheader("📊 Tabla de Datos (Estilo Screaming Frog)")
    
    # Función de estilo mejorada para legibilidad
    def style_seo_table(v):
        if not isinstance(v, (int, float)): return ''
        if v < 60: return 'background-color: #d9534f; color: white; font-weight: bold;' # Rojo fuerte
        if v < 90: return 'background-color: #f0ad4e; color: black; font-weight: bold;' # Naranja
        return 'background-color: #5cb85c; color: white; font-weight: bold;' # Verde fuerte

    display_cols = ['url', 'seo_score', 'status_code', 'schema_detected', 'internal_links', 'h1_count', 'content_type']
    st.dataframe(
        df[display_cols].style.applymap(style_seo_table, subset=['seo_score']), 
        use_container_width=True
    )

    # --- 4. EXPORTACIÓN ---
    st.download_button("📥 Descargar Reporte CSV", data=to_csv_bytes(df), file_name="auditoria_deseo.csv")

elif not urls and 's_url' in locals():
    st.info("Introduce una fuente de datos para comenzar el análisis.")

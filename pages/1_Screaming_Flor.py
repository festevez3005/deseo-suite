import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from seo_logic import audit_one, load_sitemap_urls, to_csv_bytes, get_glossary

st.set_page_config(page_title="Screaming Flor - Auditoría Pro", layout="wide")

st.title("🌸 Screaming Flor: Auditoría Pro")

# --- GLOSARIO DINÁMICO ---
with st.expander("📖 Glosario de Conceptos"):
    glossary = get_glossary()
    cols = st.columns(2)
    for i, (term, definition) in enumerate(glossary.items()):
        cols[i % 2].markdown(f"**{term}:** {definition}")

# --- CONFIGURACIÓN ---
st.sidebar.header("Configuración")
mode = st.sidebar.radio("Fuente", ["Sitemap XML", "Lista Manual"])
max_pages = st.sidebar.slider("Límite de páginas", 10, 100, 50)

urls = []
if mode == "Sitemap XML":
    s_url = st.text_input("URL del Sitemap")
    if s_url: urls = load_sitemap_urls(s_url, max_pages)
else:
    t_area = st.text_area("URLs (una por línea)")
    if t_area: urls = [u.strip() for u in t_area.splitlines() if u.strip()][:max_pages]

if st.button("🚀 Ejecutar Auditoría", type="primary") and urls:
    with st.status("Rastreando sitio...", expanded=True) as status:
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(audit_one, u): u for u in urls}
            for i, fut in enumerate(as_completed(futures)):
                results.append(fut.result())
        status.update(label="¡Auditoría Completa!", state="complete", expanded=False)

    df = pd.DataFrame(results)

    # --- 1. ALERTAS CRÍTICAS (Lo más importante arriba) ---
    all_issues = [issue for sublist in df['critical_issues'] for issue in sublist]
    if all_issues:
        st.subheader("🚨 Errores Críticos Detectados")
        # Mostrar los 3 errores más comunes
        issue_counts = pd.Series(all_issues).value_counts()
        for issue, count in issue_counts.items():
            st.error(f"**{issue}:** Encontrado en {count} páginas.")

    # --- 2. RESUMEN VISUAL ---
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Salud Promedio", f"{int(df['seo_score'].mean())}/100")
    c2.metric("Páginas HTML", len(df[df['content_type'] == 'HTML']))
    c3.metric("Tiempo Carga Promedio", f"{df['response_time'].mean():.2f}s")

    # Gráfico de Status (Pie Chart para ver la salud de un vistazo)
    st.subheader("📈 Estado General de Respuestas (HTTP Status)")
    status_counts = df['status_code'].value_counts()
    st.bar_chart(status_counts)

    # --- 3. TABLA ESTILO SCREAMING FROG ---
    st.subheader("📊 Tabla de Datos (Estilo Screaming Frog)")
    
    # Formatear la tabla para que sea legible
    display_df = df[['url', 'seo_score', 'status_code', 'content_type', 'h1_count', 'title_len', 'response_time']]
    
    def highlight_score(s):
        return ['background-color: #ffcccc' if v < 60 else 'background-color: #e6ffed' if v > 85 else '' for v in s]

    st.dataframe(display_df.style.apply(highlight_score, subset=['seo_score']), use_container_width=True)

    # --- 4. EXPORTACIÓN ---
    st.download_button("⬇️ Descargar Reporte CSV", data=to_csv_bytes(df), file_name="deseo_full_audit.csv")

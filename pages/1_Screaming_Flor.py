import streamlit as st
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from seo_logic import audit_one, load_sitemap_urls, to_csv_bytes, get_educational_legend

st.set_page_config(page_title="DeSeo - Auditoría Masiva", layout="wide")

st.title("🌸 Screaming Flor: Auditoría de Sitio")

# --- LEYENDAS EDUCATIVAS ---
with st.expander("📚 Guía rápida: ¿Qué estamos analizando?"):
    legends = get_educational_legend()
    for key, text in legends.items():
        st.write(f"**{key.replace('_', ' ').title()}:** {text}")

# --- ENTRADA ---
st.sidebar.header("Configuración")
mode = st.sidebar.radio("Fuente de datos", ["Sitemap XML", "Lista Manual"])
max_pages = st.sidebar.slider("Límite de páginas", 5, 50, 20)

urls = []
if mode == "Sitemap XML":
    s_url = st.text_input("URL del Sitemap", placeholder="https://tusitio.com/sitemap.xml")
    if s_url: urls = load_sitemap_urls(s_url, max_pages)
else:
    t_area = st.text_area("Pega tus URLs (una por línea)")
    if t_area: urls = [u.strip() for u in t_area.splitlines() if u.strip()][:max_pages]

if st.button("🚀 Iniciar Auditoría Masiva", type="primary") and urls:
    results = []
    progress = st.progress(0)
    status = st.empty()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(audit_one, u): u for u in urls}
        for i, fut in enumerate(as_completed(futures)):
            results.append(fut.result())
            progress.progress((i + 1) / len(urls))
            status.text(f"Procesando {i+1} de {len(urls)}...")

    df = pd.DataFrame(results)
    
    # --- VISUALIZACIÓN ---
    st.divider()
    
    # KPIs Generales
    c1, c2, c3 = st.columns(3)
    c1.metric("Salud Promedio", f"{int(df['seo_score'].mean())}/100")
    c2.metric("Páginas con Error", len(df[df['status_code'] != 200]))
    c3.metric("Promedio Carga", f"{df['response_time'].mean():.2f}s")

    # Tabla Interactiva
    st.subheader("📊 Resultados Detallados")
    
    # Aplicar colores al dataframe (opcional pero muy útil)
    def color_score(val):
        color = 'red' if val < 60 else 'orange' if val < 90 else 'green'
        return f'color: {color}; font-weight: bold'

    st.dataframe(df.style.applymap(color_score, subset=['seo_score']), use_container_width=True)

    # Descarga
    st.download_button("📥 Descargar Reporte para Alumnos", data=to_csv_bytes(df), file_name="auditoria_deseo.csv")

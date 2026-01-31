import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from seo_logic.py import audit_one, to_csv_bytes # Asegúrate de tener estas funciones en seo_logic

st.set_page_config(page_title="DeSeo - Screaming Flor", layout="wide")

st.title("🌸 Screaming Flor: Diagnóstico SEO")
st.markdown("Analiza los elementos vitales de tu web y mejora tu puntuación.")

# --- ENTRADA DE DATOS ---
col_in, col_set = st.columns([2, 1])
with col_in:
    url_to_test = st.text_input("URL a analizar", placeholder="https://ejemplo.com")
with col_set:
    concurrency = st.slider("Velocidad de rastreo", 1, 10, 5)

if st.button("🚀 Iniciar Análisis", type="primary"):
    if url_to_test:
        with st.spinner("Escaneando sitio..."):
            # En este ejemplo analizamos una sola, pero la lógica ThreadPool sirve para listas
            data = audit_one(url_to_test)
            df = pd.DataFrame([data])
        
        # --- CABECERA DE RESULTADOS ---
        score = data["seo_score"]
        st.divider()
        c1, c2 = st.columns([1, 3])
        with c1:
            st.metric("SEO Score", f"{score}/100")
        with c2:
            if score == 100: st.balloons(); st.success("¡Tu página es un ejemplo a seguir!")
            elif score > 70: st.info("Vas por buen camino, pero hay detalles por pulir.")
            else: st.warning("Hay problemas críticos que están afectando tu posicionamiento.")

        # --- TABS ---
        t_diag, t_tech, t_content = st.tabs(["🎯 Diagnóstico", "🌐 Técnico", "📝 On-Page"])
        
        with t_diag:
            st.subheader("Hoja de Ruta")
            st.write(f"**Recomendación principal:** {data['recommendation']}")
            # Aquí podrías listar los errores detectados de forma humana
            if score < 100:
                st.write("### Tareas pendientes:")
                if data["h1_count"] != 1: st.error("- Corregir los encabezados H1 (debe haber exactamente uno).")
                if data["title_status"] != "🟢 Perfecto": st.warning("- Ajustar la extensión del título SEO.")
                if data["img_no_alt"] > 0: st.info(f"- Añadir texto ALT a las {data['img_no_alt']} imágenes faltantes.")

        with t_tech:
            st.json({"Status Code": data["status_code"], "H1 Count": data["h1_count"]})

        with t_content:
            st.write(f"**Título:** {data['title']} ({data['title_status']})")
            st.write(f"**Meta Descripción:** {data['meta_desc']} ({data['desc_status']})")

    else:
        st.error("Por favor, ingresa una URL válida.")

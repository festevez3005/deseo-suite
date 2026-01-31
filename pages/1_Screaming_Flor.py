import streamlit as st
import pandas as pd
from seo_logic import audit_one, to_csv_bytes

# Estilo para mejorar la legibilidad de la tabla
st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# ... (Lógica de ejecución similar a la anterior) ...

if st.button("🚀 Ejecutar Auditoría", type="primary") and urls:
    # ... (Procesamiento con ThreadPoolExecutor) ...
    df = pd.DataFrame(results)

    # --- NUEVA SECCIÓN: DASHBOARD DE ESTRATEGIA ---
    st.subheader("💡 Análisis Estratégico")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Datos Estructurados (Schema)**")
        con_schema = len(df[df['schema_detected'] != "No"])
        st.info(f"Páginas con Schema: {con_schema} de {len(df)}")
        st.caption("El Schema ayuda a Google y a las IAs a entender si eres un Producto, Receta, Artículo u Organización.")

    with col2:
        st.write("**Arquitectura de Enlaces**")
        avg_int = df['internal_links'].mean()
        st.success(f"Promedio de enlaces internos: {avg_int:.1f}")
        st.caption("Los enlaces internos ayudan a distribuir la 'autoridad' de tu sitio entre tus páginas.")

    # --- TABLA ESTILO SCREAMING FROG (Mejorada) ---
    st.subheader("📊 Auditoría Técnica Detallada")

    def style_final(val):
        """Función de color con texto negro para legibilidad"""
        if isinstance(val, int):
            if val < 60: return 'background-color: #ff4b4b; color: white;'
            if val < 90: return 'background-color: #ffa500; color: black;'
            return 'background-color: #2eb82e; color: white;' # Verde fuerte, texto blanco
        return ''

    # Reordenamos columnas para dar prioridad a lo nuevo
    display_cols = ['url', 'seo_score', 'status_code', 'schema_detected', 'internal_links', 'h1_count', 'content_type']
    st.dataframe(df[display_cols].style.applymap(style_final, subset=['seo_score']), use_container_width=True)

    # Exportación
    st.download_button("📥 Descargar Reporte Completo", data=to_csv_bytes(df), file_name="audit_deseo.csv")

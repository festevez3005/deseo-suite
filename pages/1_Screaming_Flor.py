# Dentro del loop de resultados de tu archivo de página:
st.header("📋 Diagnóstico de Páginas")

for index, row in df.iterrows():
    # Creamos un título con color según el estado
    emoji = "🟢" if row['status'] == "✅ OK" else "🔴"
    with st.expander(f"{emoji} {row['url']}"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**SEO Técnico**")
            st.write(f"Status: {row['status_code']}")
            st.write(f"H1: {row['h1_status']}")
            
        with col2:
            st.write("**Contenido**")
            st.write(f"Título: {row['title_status']} ({row['title_len']} car.)")
            st.write(f"Meta Desc: {row['desc_status']} ({row['desc_len']} car.)")
            
        with col3:
            st.write("**Accesibilidad**")
            st.write(f"Imágenes: {row['alt_status']}")

        st.warning(f"💡 **Recomendación DeSeo:** {row['recommendation']}")

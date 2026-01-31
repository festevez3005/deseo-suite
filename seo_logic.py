def audit_one(url: str, base_domain: str | None = None, timeout: int = 15) -> dict:
    out = {"url": url, "status": "✅ OK", "recommendation": "Ninguna"}
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # --- 1. Salud Técnica ---
        out["status_code"] = r.status_code
        if r.status_code != 200:
            out["status"] = "❌ Error"
            out["recommendation"] = "Revisar por qué la página no carga (posible 404 o error de servidor)."

        # --- 2. Títulos y Metas con Validación ---
        title = soup.title.string.strip() if soup.title else ""
        out["title"] = title
        out["title_len"] = len(title)
        if len(title) < 30:
            out["title_status"] = "🟡 Muy corto"
        elif len(title) > 65:
            out["title_status"] = "🟡 Muy largo"
        else:
            out["title_status"] = "🟢 Perfecto"

        desc = extract_meta(soup, "description")
        out["meta_desc"] = desc
        out["desc_len"] = len(desc)
        if len(desc) < 120:
            out["desc_status"] = "🟡 Muy corta"
        elif len(desc) > 160:
            out["desc_status"] = "🟡 Muy larga"
        else:
            out["desc_status"] = "🟢 Perfecta"

        # --- 3. Jerarquía H1-H3 ---
        h1s = soup.find_all("h1")
        out["h1_count"] = len(h1s)
        if len(h1s) == 0:
            out["h1_status"] = "🔴 Falta H1"
        elif len(h1s) > 1:
            out["h1_status"] = "🟡 Más de un H1"
        else:
            out["h1_status"] = "🟢 Correcto"

        out["h2_count"] = len(soup.find_all("h2"))
        out["h3_count"] = len(soup.find_all("h3"))

        # --- 4. Imágenes y ALT ---
        imgs = soup.find_all("img")
        missing_alt = sum(1 for img in imgs if not img.get("alt"))
        out["img_total"] = len(imgs)
        out["img_no_alt"] = missing_alt
        out["alt_status"] = "🟢 OK" if missing_alt == 0 else f"🔴 {missing_alt} sin texto ALT"

    except Exception as e:
        out["status"] = "❌ Error crítico"
        out["recommendation"] = f"Error de conexión: {str(e)}"
    
    return out

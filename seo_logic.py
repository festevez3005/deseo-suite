import requests
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_glossary():
    return {
        "Status Code": "Indica si la página cargó bien (200), no existe (404) o tiene errores de servidor (500).",
        "SEO Score": "Calificación de 0 a 100 basada en qué tan bien optimizada está la página técnicamente.",
        "Tipo de Recurso": "Identifica si el enlace es una página (HTML), una imagen, un script (JS) o un estilo (CSS).",
        "H1 (Título Interno)": "Es el encabezado principal. Google lo usa para entender el tema central de la página.",
        "SEO Title": "Es el título que aparece en la pestaña del navegador y en los resultados de Google.",
        "Meta Description": "Breve resumen que aparece bajo el título en Google. Influye en si la gente hace clic o no.",
        "Alt Text": "Descripción de imagen para motores de búsqueda y personas con discapacidad visual."
    }

def detect_resource_type(content_type):
    content_type = content_type.lower()
    if "html" in content_type: return "📄 HTML"
    if "image" in content_type: return "🖼️ Imagen"
    if "javascript" in content_type or "js" in content_type: return "📜 JS"
    if "css" in content_type: return "🎨 CSS"
    if "pdf" in content_type: return "📂 PDF"
    return "📦 Otro"

def audit_one(url, timeout=15):
    out = {
        "url": url, 
        "tipo": "❓ Desconocido", 
        "status_code": "Error", 
        "seo_score": 0, 
        "response_time": 0,
        "h1_count": 0,
        "title": "",
        "img_no_alt": 0
    }
    try:
        start_time = time.time()
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        out["response_time"] = round(time.time() - start_time, 2)
        out["status_code"] = r.status_code
        
        # Detectar tipo de recurso
        ct = r.headers.get("Content-Type", "")
        out["tipo"] = detect_resource_type(ct)

        # Solo auditar SEO si es HTML
        if "📄 HTML" in out["tipo"]:
            soup = BeautifulSoup(r.text, "html.parser")
            
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            out["title"] = title
            out["title_len"] = len(title)
            
            h1s = soup.find_all("h1")
            out["h1_count"] = len(h1s)
            
            imgs = soup.find_all("img")
            out["img_total"] = len(imgs)
            out["img_no_alt"] = sum(1 for img in imgs if not img.get("alt"))
            
            # Score
            score = 100
            if r.status_code != 200: score -= 50
            if len(h1s) != 1: score -= 20
            if not (30 <= len(title) <= 65): score -= 15
            if out["img_no_alt"] > 0: score -= 5
            out["seo_score"] = max(0, score)
        else:
            out["seo_score"] = "N/A" # No aplica a imágenes/JS

    except:
        pass
    return out

def load_sitemap_urls(sitemap_url, max_urls=100):
    try:
        r = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        root = ET.fromstring(r.content)
        urls = [loc.text for loc in root.findall(".//{*}loc")]
        return [u for u in urls if u and u.startswith("http")][:max_urls]
    except:
        return []

def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")

import requests
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time  # Agregado para evitar errores de medición de tiempo

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_educational_legend():
    return {
        "status_code": "El código de respuesta indica si la página es accesible. 200 es OK, 404 es no encontrada y 500 es error de servidor.",
        "h1": "El H1 es el título principal. Debe haber solo uno y contener la palabra clave principal.",
        "title": "Es lo primero que el usuario ve en Google. Debe tener entre 30 y 65 caracteres.",
        "meta_desc": "Es el resumen que aparece en Google. Debe invitar al clic.",
        "alt_text": "Es la descripción de las imágenes para personas con discapacidad visual y para Google."
    }

def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")

def load_sitemap_urls(sitemap_url, max_urls=50):
    try:
        r = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        # Intentar parsear el XML de forma robusta
        root = ET.fromstring(r.content)
        # Buscar 'loc' sin importar el namespace (usando wildcards)
        urls = [loc.text for loc in root.findall(".//{*}loc")]
        return [u for u in urls if u and u.startswith("http")][:max_urls]
    except Exception as e:
        print(f"Error cargando sitemap: {e}")
        return []

def audit_one(url, timeout=15):
    out = {"url": url, "seo_score": 0, "status_code": "Error", "response_time": 0}
    try:
        start_time = time.time()
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        out["response_time"] = round(time.time() - start_time, 2)
        out["status_code"] = r.status_code
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        # On-Page
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        out["title"] = title
        out["title_len"] = len(title)
        
        h1s = soup.find_all("h1")
        out["h1_count"] = len(h1s)
        
        imgs = soup.find_all("img")
        out["img_total"] = len(imgs)
        out["img_no_alt"] = sum(1 for img in imgs if not img.get("alt"))
        
        # Scoring Pedagógico
        score = 100
        if r.status_code != 200: score -= 50
        if len(h1s) != 1: score -= 20
        if not (30 <= len(title) <= 65): score -= 15
        if out["img_no_alt"] > 0: score -= 5
        
        out["seo_score"] = max(0, score)
    except:
        pass
    return out

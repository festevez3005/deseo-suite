import requests
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_educational_legend():
    return {
        "status_code": "El código de respuesta indica si la página es accesible. 200 es OK, 404 es no encontrada y 500 es error de servidor.",
        "h1": "El H1 es el título principal de la página. Debe haber solo uno y contener la palabra clave principal.",
        "title": "Es lo primero que el usuario ve en Google. Debe tener entre 30 y 65 caracteres.",
        "meta_desc": "Es el texto que invita a hacer clic en los resultados de búsqueda. Debe ser persuasivo.",
        "alt_text": "Es la descripción de las imágenes para personas con discapacidad visual y para que Google entienda la foto."
    }

def load_sitemap_urls(sitemap_url, max_urls=50):
    try:
        r = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        root = ET.fromstring(r.content)
        # Manejo simple de namespaces de sitemaps
        urls = [loc.text for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        return urls[:max_urls]
    except:
        return []

def audit_one(url, timeout=15):
    started = time.time() if 'time' in globals() else 0
    out = {"url": url, "seo_score": 0}
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Performance básica (Tiempo de respuesta)
        out["response_time"] = round(r.elapsed.total_seconds(), 2)
        out["status_code"] = r.status_code
        
        # On-Page
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        out["title"] = title
        out["title_len"] = len(title)
        
        h1s = soup.find_all("h1")
        out["h1_count"] = len(h1s)
        
        imgs = soup.find_all("img")
        out["img_total"] = len(imgs)
        out["img_no_alt"] = sum(1 for img in imgs if not img.get("alt"))
        
        # Scoring simple
        score = 100
        if r.status_code != 200: score -= 50
        if len(h1s) != 1: score -= 20
        if not (30 <= len(title) <= 65): score -= 15
        out["seo_score"] = max(0, score)
        
    except:
        out["status_code"] = "Error"
        out["seo_score"] = 0
    return out

def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")

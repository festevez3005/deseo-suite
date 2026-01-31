import requests
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_glossary():
    return {
        "Status Code": "Estado de la página. 200 es éxito, 404 es no encontrada, 301 es redirección.",
        "Content Type": "Tipo de archivo detectado (HTML, imagen, PDF, etc.). Solo el HTML suma puntos SEO.",
        "SEO Score": "Puntaje de 0 a 100 basado en la salud técnica y on-page de la URL.",
        "H1": "Título principal del contenido. Es vital para que Google sepa de qué trata la página.",
        "Meta Description": "El texto que aparece bajo el título en Google. Influye en si la gente hace clic o no.",
        "Alt Text": "Descripción de imagen. Ayuda a la accesibilidad y al SEO de imágenes."
    }

def load_sitemap_urls(sitemap_url, max_urls=100):
    try:
        r = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        root = ET.fromstring(r.content)
        urls = [loc.text for loc in root.findall(".//{*}loc")]
        return [u for u in urls if u and u.startswith("http")][:max_urls]
    except:
        return []

def audit_one(url, timeout=15):
    out = {
        "url": url, "status_code": "Error", "content_type": "Desconocido",
        "seo_score": 0, "response_time": 0, "h1_count": 0, "title": "", 
        "title_len": 0, "meta_desc": "", "img_no_alt": 0, "critical_issues": []
    }
    try:
        start_time = time.time()
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        out["response_time"] = round(time.time() - start_time, 2)
        out["status_code"] = r.status_code
        
        # Detectar tipo de contenido
        ctype = r.headers.get("Content-Type", "").lower()
        if "html" in ctype: out["content_type"] = "HTML"
        elif "image" in ctype: out["content_type"] = "Imagen"
        elif "javascript" in ctype: out["content_type"] = "JS"
        elif "css" in ctype: out["content_type"] = "CSS"
        else: out["content_type"] = "Otro"

        if out["content_type"] == "HTML":
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Análisis On-page
            title_tag = soup.find("title")
            out["title"] = title_tag.string.strip() if title_tag and title_tag.string else ""
            out["title_len"] = len(out["title"])
            
            desc_tag = soup.find("meta", attrs={"name": "description"})
            out["meta_desc"] = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""
            
            h1s = soup.find_all("h1")
            out["h1_count"] = len(h1s)
            
            imgs = soup.find_all("img")
            out["img_no_alt"] = sum(1 for img in imgs if not img.get("alt"))

            # Detección de Errores Críticos
            if r.status_code != 200: out["critical_issues"].append("⚠️ Error de acceso (Status != 200)")
            if out["h1_count"] == 0: out["critical_issues"].append("🔴 Falta H1")
            if out["h1_count"] > 1: out["critical_issues"].append("🟡 Múltiples H1")
            if out["title_len"] == 0: out["critical_issues"].append("🔴 Sin Title")
            if not out["meta_desc"]: out["critical_issues"].append("🟡 Sin Meta Description")
            
            # Scoring
            score = 100
            if r.status_code != 200: score -= 50
            if out["h1_count"] != 1: score -= 20
            if not (30 <= out["title_len"] <= 65): score -= 15
            if not out["meta_desc"]: score -= 10
            out["seo_score"] = max(0, score)
        else:
            out["seo_score"] = 100 if r.status_code == 200 else 0

    except:
        out["critical_issues"].append("❌ Error de conexión")
    
    return out

def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")

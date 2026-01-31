import requests
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
from urllib.parse import urlparse

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_glossary():
    return {
        "Status Code": "Código de respuesta del servidor (200=OK, 404=No encontrado, 301/302=Redirección).",
        "Schema Markup": "Fragmentos de código (JSON-LD) que ayudan a buscadores e IAs a entender el contexto de tu página.",
        "Internal Links": "Enlaces que apuntan a otras páginas de tu propio dominio. Clave para la navegación.",
        "External Links": "Enlaces que apuntan a sitios fuera de tu dominio.",
        "SEO Score": "Calificación de 0 a 100 basada en la salud técnica y optimización on-page de la URL.",
        "H1": "El encabezado principal. Debe ser único y describir claramente el tema central."
    }

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

def audit_one(url, timeout=15):
    out = {
        "url": url, "status_code": "Error", "content_type": "Otro",
        "seo_score": 0, "response_time": 0, "h1_count": 0, "title_len": 0, 
        "schema_detected": "No", "internal_links": 0, "external_links": 0, "critical_issues": []
    }
    try:
        start_time = time.time()
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        out["response_time"] = round(time.time() - start_time, 2)
        out["status_code"] = r.status_code
        
        # Detección de Tipo de Contenido
        ctype = r.headers.get("Content-Type", "").lower()
        if "html" in ctype:
            out["content_type"] = "HTML"
            soup = BeautifulSoup(r.text, "html.parser")
            
            # 1. Schema Markup (JSON-LD)
            schemas = soup.find_all("script", type="application/ld+json")
            if schemas:
                out["schema_detected"] = f"Sí ({len(schemas)} bloques)"
            else:
                out["critical_issues"].append("🟡 Sin Schema Markup (JSON-LD)")

            # 2. Linking Interno / Externo
            domain = urlparse(url).netloc
            links = soup.find_all("a", href=True)
            int_l, ext_l = 0, 0
            for link in links:
                href = link['href']
                if href.startswith("/") or (domain and domain in href):
                    int_l += 1
                else:
                    ext_l += 1
            out["internal_links"] = int_l
            out["external_links"] = ext_l

            # 3. On-Page Tradicional
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            out["title_len"] = len(title)
            h1s = soup.find_all("h1")
            out["h1_count"] = len(h1s)
            
            # Scoring
            score = 100
            if r.status_code != 200: score -= 50; out["critical_issues"].append("⚠️ Error Status")
            if len(h1s) != 1: score -= 20; out["critical_issues"].append("🔴 Problema con H1")
            if not (

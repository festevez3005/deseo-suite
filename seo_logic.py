import requests
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
from urllib.parse import urlparse

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_glossary():
    return {
        "Status Code": "Código de respuesta (200=OK, 404=No encontrado).",
        "Schema Markup": "Datos estructurados JSON-LD para buscadores e IAs.",
        "Internal Links": "Enlaces hacia tu propio dominio.",
        "SEO Score": "Puntaje de salud de 0 a 100.",
        "Title": "El título que aparece en la pestaña del navegador y en Google.",
        "Meta Description": "El resumen descriptivo que aparece en los resultados de búsqueda."
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
        "seo_score": 0, "response_time": 0, "h1_count": 0, 
        "title": "", "title_len": 0, "meta_desc": "", "meta_desc_len": 0,
        "schema_detected": "No", "internal_links": 0, "critical_issues": []
    }
    try:
        start_time = time.time()
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        out["response_time"] = round(time.time() - start_time, 2)
        out["status_code"] = r.status_code
        
        ctype = r.headers.get("Content-Type", "").lower()
        if "html" in ctype:
            out["content_type"] = "HTML"
            soup = BeautifulSoup(r.text, "html.parser")
            
            # 1. Schema
            schemas = soup.find_all("script", type="application/ld+json")
            out["schema_detected"] = f"Sí ({len(schemas)})" if schemas else "No"

            # 2. Linking
            domain = urlparse(url).netloc
            links = soup.find_all("a", href=True)
            out["internal_links"] = sum(1 for l in links if l['href'].startswith("/") or (domain and domain in l['href']))

            # 3. Title & Meta Description (NUEVO)
            t_tag = soup.find("title")
            out["title"] = t_tag.string.strip() if t_tag and t_tag.string else ""
            out["title_len"] = len(out["title"])

            d_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            out["meta_desc"] = d_tag["content"].strip() if d_tag and d_tag.get("content") else ""
            out["meta_desc_len"] = len(out["meta_desc"])
            
            # 4. H1
            h1s = soup.find_all("h1")
            out["h1_count"] = len(h1s)
            
            # Scoring
            score = 100
            if r.status_code != 200: score -= 50
            if len(h1s) != 1: score -= 20
            if not (30 <= out["title_len"] <= 65): score -= 15
            if out["meta_desc_len"] == 0: score -= 10
            out["seo_score"] = max(0, score)
        else:
            out["content_type"] = ctype.split(';')[0]
            out["seo_score"] = 100 if r.status_code == 200 else 0
    except:
        pass
    return out

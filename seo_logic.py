import requests
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def extract_meta(soup, name):
    tag = soup.find("meta", attrs={"name": name}) or soup.find("meta", attrs={"property": name})
    return tag["content"].strip() if tag and tag.get("content") else ""

def calculate_seo_score(data):
    score = 100
    if data["status_code"] != 200: score -= 50
    if data["h1_count"] != 1: score -= 20
    if data["title_status"] != "🟢 Perfecto": score -= 15
    if data["desc_status"] != "🟢 Perfecta": score -= 10
    if data["img_no_alt"] > 0: score -= 5
    return max(0, score)

def audit_one(url, timeout=15):
    out = {"url": url, "recommendation": "¡Buen trabajo! Sigue así."}
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        soup = BeautifulSoup(r.text, "html.parser")
        out["status_code"] = r.status_code

        # --- Título ---
        title = soup.title.string.strip() if soup.title else ""
        out["title"] = title
        out["title_len"] = len(title)
        if len(title) == 0: out["title_status"] = "🔴 Falta"; out["recommendation"] = "El título es obligatorio para SEO."
        elif len(title) < 30: out["title_status"] = "🟡 Corto"
        elif len(title) > 65: out["title_status"] = "🟡 Largo"
        else: out["title_status"] = "🟢 Perfecto"

        # --- Meta Desc ---
        desc = extract_meta(soup, "description")
        out["meta_desc"] = desc
        out["desc_len"] = len(desc)
        if len(desc) == 0: out["desc_status"] = "🔴 Falta"
        elif len(desc) < 120: out["desc_status"] = "🟡 Corta"
        elif len(desc) > 160: out["desc_status"] = "🟡 Larga"
        else: out["desc_status"] = "🟢 Perfecta"

        # --- Encabezados ---
        h1s = soup.find_all("h1")
        out["h1_count"] = len(h1s)
        out["h1_status"] = "🟢 OK" if len(h1s) == 1 else "🔴 Error"
        out["h2_count"] = len(soup.find_all("h2"))
        out["h3_count"] = len(soup.find_all("h3"))

        # --- Imágenes ---
        imgs = soup.find_all("img")
        out["img_total"] = len(imgs)
        out["img_no_alt"] = sum(1 for img in imgs if not img.get("alt"))
        out["alt_status"] = "🟢 OK" if out["img_no_alt"] == 0 else f"🔴 {out['img_no_alt']} sin ALT"

        # Score Final
        out["seo_score"] = calculate_seo_score(out)

    except Exception as e:
        out.update({"status_code": 0, "seo_score": 0, "recommendation": f"Error de conexión: {e}"})
    
    return out

# Reutiliza tus funciones normalize_url y load_sitemap_urls aquí...

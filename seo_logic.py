import requests
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
import json

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def audit_one(url, timeout=15):
    out = {
        "url": url, "status_code": "Error", "content_type": "Otro",
        "seo_score": 0, "h1_count": 0, "schema_detected": "No",
        "internal_links": 0, "external_links": 0, "critical_issues": []
    }
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        out["status_code"] = r.status_code
        ctype = r.headers.get("Content-Type", "").lower()
        
        if "html" in ctype:
            out["content_type"] = "HTML"
            soup = BeautifulSoup(r.text, "html.parser")
            
            # --- 1. Detección de Schema Markup ---
            schemas = soup.find_all("script", type="application/ld+json")
            if schemas:
                out["schema_detected"] = f"Sí ({len(schemas)} bloques)"
            else:
                out["critical_issues"].append("🟡 Sin Schema Markup (JSON-LD)")

            # --- 2. Análisis de Enlaces (Linking) ---
            domain = urlparse(url).netloc
            links = soup.find_all("a", href=True)
            int_l, ext_l = 0, 0
            for link in links:
                href = link['href']
                if href.startswith("/") or domain in href:
                    int_l += 1
                else:
                    ext_l += 1
            out["internal_links"] = int_l
            out["external_links"] = ext_l
            
            if int_l == 0: out["critical_issues"].append("🟡 Sin enlaces internos")

            # --- 3. On-Page Clásico ---
            h1s = soup.find_all("h1")
            out["h1_count"] = len(h1s)
            title = soup.title.string.strip() if soup.title else ""
            out["title_len"] = len(title)
            
            # Scoring
            score = 100
            if r.status_code != 200: score -= 50
            if len(h1s) != 1: score -= 20
            if not schemas: score -= 10 # Penalizamos falta de Schema
            out["seo_score"] = max(0, score)
        else:
            out["content_type"] = "Media/Otro"
            out["seo_score"] = 100 if r.status_code == 200 else 0
            
    except:
        out["critical_issues"].append("❌ Error de conexión")
    return out

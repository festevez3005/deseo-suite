import requests
import pandas as pd
import gzip
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests.exceptions import RequestException
import xml.etree.ElementTree as ET

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def normalize_url(u: str) -> str:
    u = (u or "").strip()
    if not u: return ""
    if u.startswith("www."): u = "https://" + u
    return u

def fetch_bytes(url: str, timeout: int = 15) -> bytes:
    r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return r.content

def parse_sitemap_xml(xml_bytes: bytes):
    sitemaps, urls = [], []
    root = ET.fromstring(xml_bytes)
    def findall_local(tag_name: str): return root.findall(f".//{{*}}{tag_name}")
    sitemap_locs = [el.text.strip() for el in findall_local("sitemap") for el in el.findall(".//{*}loc") if el.text]
    if sitemap_locs:
        sitemaps.extend(sitemap_locs)
        return sitemaps, urls
    locs = [el.text.strip() for el in findall_local("loc") if el.text]
    urls.extend(locs)
    return sitemaps, urls

def load_sitemap_urls(sitemap_url: str, max_urls: int = 300) -> list[str]:
    sitemap_url = normalize_url(sitemap_url)
    if not sitemap_url: return []
    collected, to_process, seen = [], [sitemap_url], set()
    while to_process and len(collected) < max_urls:
        current = to_process.pop(0)
        if current in seen: continue
        seen.add(current)
        try:
            content = fetch_bytes(current)
            if current.endswith(".gz"): content = gzip.decompress(content)
            sitemaps, urls = parse_sitemap_xml(content)
            for sm in sitemaps:
                sm = normalize_url(sm)
                if sm and sm not in seen: to_process.append(sm)
            for u in urls:
                u = normalize_url(u)
                if u and u not in collected:
                    collected.append(u)
                    if len(collected) >= max_urls: break
        except Exception: continue
    return collected

def audit_one(url: str, base_domain: str | None = None, timeout: int = 15) -> dict:
    # Aquí va toda tu lógica de BeautifulSoup (la que ya tenías)
    # [Asegúrate de pegar aquí la función completa que tenías antes]
    return {"url": url, "status_code": 200} # Resumen por brevedad

def add_issue_flags(df: pd.DataFrame) -> pd.DataFrame:
    # Aquí va toda tu lógica de flags de errores (la que ya tenías)
    return df

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")

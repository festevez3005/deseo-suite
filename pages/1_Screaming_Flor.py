import streamlit as st
import requests
import pandas as pd
import gzip
import time
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import xml.etree.ElementTree as ET

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="DeSeo - Screaming Flor",
    layout="wide"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ==================================================
# HELPERS
# ==================================================

def normalize_url(url):
    url = (url or "").strip()

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def fetch_bytes(url):

    for _ in range(3):

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=15
            )

            response.raise_for_status()

            return response.content

        except Exception:
            time.sleep(1)

    return None


def parse_sitemap(xml_bytes):

    urls = []

    try:

        root = ET.fromstring(xml_bytes)

        for loc in root.findall(".//{*}loc"):

            if loc.text:
                urls.append(loc.text.strip())

    except Exception as e:

        st.warning(f"Error parseando sitemap: {e}")

    return urls


def load_sitemap(sitemap_url, max_urls=20):

    content = fetch_bytes(sitemap_url)

    if not content:
        return []

    try:

        if sitemap_url.endswith(".gz"):
            content = gzip.decompress(content)

    except Exception:
        pass

    urls = parse_sitemap(content)

    return urls[:max_urls]


# ==================================================
# AUDITORÍA
# ==================================================

def audit_url(url):

    result = {
        "url": url
    }

    start = time.time()

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        result["status_code"] = response.status_code

        result["response_ms"] = int(
            (time.time() - start) * 1000
        )

        if response.status_code != 200:
            return result

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # eliminar scripts/styles
        for tag in soup(["script", "style"]):
            tag.decompose()

        # =========================
        # TITLE
        # =========================

        title = ""

        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        # =========================
        # META DESCRIPTION
        # =========================

        meta_description = ""

        meta_tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta_tag and meta_tag.get("content"):
            meta_description = meta_tag.get("content").strip()

        # =========================
        # H1
        # =========================

        h1_tags = soup.find_all("h1")

        # =========================
        # WORD COUNT
        # =========================

        text = soup.get_text(separator=" ")

        text = re.sub(r"\s+", " ", text)

        word_count = len(text.split())

        # =========================
        # RESULT
        # =========================

        result.update({
            "title": title,
            "title_len": len(title),

            "meta_description": meta_description,
            "meta_description_len": len(meta_description),

            "h1_count": len(h1_tags),

            "word_count": word_count
        })

    except Exception as e:

        result["error"] = str(e)

    return result


# ==================================================
# SEO SCORE
# ==================================================

def compute_score(row):

    score = 0

    status_code = row.get("status_code") or 0
    title_len = row.get("title_len") or 0
    meta_description_len = row.get("meta_description_len") or 0
    h1_count = row.get("h1_count") or 0
    word_count = row.get("word_count") or 0

    # Status 200
    if status_code == 200:
        score += 20

    # Title OK
    if 10 <= title_len <= 70:
        score += 20

    # Meta description OK
    if 50 <= meta_description_len <= 160:
        score += 20

    # H1 OK
    if h1_count == 1:
        score += 20

    # Content OK
    if word_count > 300:
        score += 20

    return score


def score_label(score):

    if score >= 80:
        return "🟢 Alto"

    elif score >= 50:
        return "🟡 Medio"

    return "🔴 Bajo"


# ==================================================
# UI
# ==================================================

st.title("🌸 DeSeo - Screaming Flor")

mode = st.radio(
    "Modo",
    ["Sitemap", "Manual"]
)

max_urls = st.slider(
    "Máximo de URLs",
    min_value=5,
    max_value=50,
    value=10
)

urls = []

# ==================================================
# SITEMAP
# ==================================================

if mode == "Sitemap":

    sitemap = st.text_input(
        "Sitemap URL",
        placeholder="https://dominio.com/sitemap.xml"
    )

    if sitemap:

        sitemap = normalize_url(sitemap)

        urls = load_sitemap(
            sitemap,
            max_urls=max_urls
        )

        st.success(f"URLs encontradas: {len(urls)}")

# ==================================================
# MANUAL
# ==================================================

else:

    text = st.text_area(
        "Pegá URLs (una por línea)"
    )

    if text:

        urls = [
            normalize_url(u)
            for u in text.splitlines()
            if u.strip()
        ][:max_urls]

# ==================================================
# RUN
# ==================================================

if st.button("🚀 Auditar"):

    if not urls:
        st.error("No hay URLs para analizar")
        st.stop()

    results = []

    progress = st.progress(0)

    with st.spinner("Auditando URLs..."):

        with ThreadPoolExecutor(
            max_workers=min(10, len(urls))
        ) as executor:

            futures = {
                executor.submit(audit_url, url): url
                for url in urls
            }

            for i, future in enumerate(as_completed(futures)):

                try:

                    results.append(
                        future.result()
                    )

                except Exception as e:

                    results.append({
                        "url": futures[future],
                        "error": str(e)
                    })

                progress.progress(
                    (i + 1) / len(urls)
                )

    # ==================================================
    # DATAFRAME
    # ==================================================

    df = pd.DataFrame(results)

    if df.empty:
        st.error("No se pudieron analizar URLs")
        st.stop()

    # columnas seguras
    default_cols = {

        "url": "",

        "status_code": None,

        "response_ms": None,

        "title": "",
        "title_len": 0,

        "meta_description": "",
        "meta_description_len": 0,

        "h1_count": 0,

        "word_count": 0,

        "error": ""
    }

    for col, default in default_cols.items():

        if col not in df.columns:
            df[col] = default

    # ==================================================
    # SEO SCORE
    # ==================================================

    df["seo_score"] = df.apply(
        compute_score,
        axis=1
    )

    df["score_label"] = df["seo_score"].apply(
        score_label
    )

    # ==================================================
    # RESULTADOS
    # ==================================================

    st.subheader("📊 Resultados")

    cols_to_show = [

        "url",

        "status_code",

        "response_ms",

        "title",
        "title_len",

        "meta_description",
        "meta_description_len",

        "h1_count",

        "word_count",

        "seo_score",

        "score_label",

        "error"
    ]

    st.dataframe(
        df[cols_to_show],
        use_container_width=True
    )

    # ==================================================
    # MÉTRICAS
    # ==================================================

    st.subheader("📈 Resumen")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "URLs auditadas",
            len(df)
        )

    with col2:

        st.metric(
            "Status 200",
            int((df["status_code"] == 200).sum())
        )

    with col3:

        st.metric(
            "SEO Score promedio",
            round(df["seo_score"].mean(), 1)
        )

    with col4:

        st.metric(
            "Tiempo promedio (ms)",
            int(df["response_ms"].fillna(0).mean())
        )

    # ==================================================
    # DOWNLOAD CSV
    # ==================================================

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇ Descargar CSV",
        data=csv,
        file_name="reporte_seo.csv",
        mime="text/csv"
    )

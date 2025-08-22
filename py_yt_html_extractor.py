#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_from_html.py – Extrahiert ein YouTube-Transkript aus lokalem HTML,
bereinigt es und exportiert eine Gesamt-TXT sowie Chunk-Dateien.

Benötigt:
  pip install beautifulsoup4 lxml
"""

import argparse
import re
import unicodedata
from pathlib import Path
from typing import List, Optional

from bs4 import BeautifulSoup


# ---------- Helpers ----------

def sanitize_title(title: str) -> str:
    """Ersetzt Umlaute & Sonderzeichen, macht einen kurzen, dateitauglichen Präfix."""
    repl = (("ä","ae"),("ö","oe"),("ü","ue"),("Ä","Ae"),("Ö","Oe"),("Ü","Ue"),("ß","ss"))
    s = title or "output"
    for a,b in repl:
        s = s.replace(a,b)
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[^A-Za-z0-9 _-]+", "", s)
    s = re.sub(r"\s+", "_", s).strip("_-")
    return (s[:100] or "output")


def get_title(soup: BeautifulSoup) -> str:
    """Bestmöglichen Titel aus dem HTML bestimmen (Header, og:title, <title>)."""
    h2 = soup.select_one("ytd-transcript-section-header-renderer h2, h2#title")
    if h2 and h2.get_text(strip=True):
        return h2.get_text(strip=True)
    og = soup.find("meta", attrs={"property": "og:title"})
    if og and og.get("content"):
        return og["content"].strip()
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "output"


def extract_segments(soup: BeautifulSoup) -> List[str]:
    """Zieht alle Segment-Texte aus typischen YouTube-Transkript-Layouts."""
    segments: List[str] = []

    # Primär: moderne Renderer
    for seg in soup.select("ytd-transcript-segment-renderer"):
        tnode = seg.select_one(".segment-text, yt-formatted-string.segment-text")
        if not tnode:
            continue
        t = tnode.get_text(separator=" ", strip=True)
        if t:
            segments.append(t)

    # Fallback: nur Klassenselektor
    if not segments:
        for node in soup.select(".segment-text, yt-formatted-string.segment-text"):
            t = node.get_text(separator=" ", strip=True)
            if t:
                segments.append(t)

    return segments


def normalize_text(s: str,
                   keep_timestamps: bool = False,
                   keep_cues: bool = False) -> str:
    """Unicode-Normalisierung, optionales Entfernen von Zeitstempeln/Cues, Whitespace säubern."""
    s = unicodedata.normalize("NFC", s.replace("\u00A0", " "))

    if not keep_cues:
        s = re.sub(r"\[(?:Music|Musik|Applause|Laughter|MUSIC|APPLAUSE|LAUGHTER)\]", "", s)

    if not keep_timestamps:
        s = re.sub(r"(\[\d{1,2}:\d{2}:\d{2}(?:\.\d{1,2})?\]|\b\d{1,2}:\d{2}(?::\d{2})?(?:\.\d{1,2})?\b)", "", s)

    s = "\n".join(re.sub(r"\s{2,}", " ", ln).strip() for ln in s.splitlines())
    s = "\n".join([ln for ln in s.splitlines() if ln.strip()])
    return s.strip()


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Zeichenbasiertes Chunking mit optionalem Overlap."""
    if chunk_size <= 0:
        raise ValueError("chunk_size muss > 0 sein")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap muss >= 0 und < chunk_size sein")
    parts: List[str] = []
    i, n = 0, len(text)
    while i < n:
        end = min(i + chunk_size, n)
        parts.append(text[i:end])
        if end == n:
            break
        i = end - overlap if overlap > 0 else end
    return parts


# ---------- Main CLI ----------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Extrahiert & säubert ein YouTube-Transkript aus lokalem HTML."
    )
    ap.add_argument("html", type=Path, help="Pfad zur gespeicherten HTML-Datei (YouTube-Seite/Transkriptansicht)")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="Optional: Ausgabeverzeichnis (Default: gleiches Verzeichnis wie die HTML-Datei)")
    ap.add_argument("--out-prefix", type=str, default=None, help="Dateipräfix überschreiben (Default: Titel aus HTML)")
    ap.add_argument("--chunk-size", type=int, default=12000, help="Zeichen pro Chunk (Default: 12000)")
    ap.add_argument("--overlap", type=int, default=500, help="Überlappung zwischen Chunks (Default: 500)")
    ap.add_argument("--keep-timestamps", action="store_true", help="Zeitstempel beibehalten")
    ap.add_argument("--keep-cues", action="store_true", help="Cues wie [Music] beibehalten")
    args = ap.parse_args()

    html_path: Path = args.html
    if not html_path.exists():
        raise SystemExit(f"Datei nicht gefunden: {html_path}")

    # Standard: gleiches Verzeichnis wie HTML
    out_dir: Path = args.out_dir or html_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    html = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "lxml")

    raw_title = get_title(soup)
    prefix = sanitize_title(raw_title) if args.out_prefix is None else sanitize_title(args.out_prefix)

    segments = extract_segments(soup)
    if not segments:
        text_joined = BeautifulSoup(html, "lxml").get_text(separator="\n", strip=True)
    else:
        text_joined = "\n".join(segments)

    clean_text = normalize_text(
        text_joined,
        keep_timestamps=args.keep_timestamps,
        keep_cues=args.keep_cues,
    )

    # Gesamtdatei
    out_single = out_dir / f"{prefix}_transcript.txt"
    out_single.write_text(clean_text + "\n", encoding="utf-8")

    # Chunks schreiben
    parts = chunk_text(clean_text, chunk_size=args.chunk_size, overlap=args.overlap)
    digits = max(3, len(str(len(parts))))
    written: List[Path] = []
    for idx, part in enumerate(parts, 1):
        p = out_dir / f"{prefix}_part_{idx:0{digits}d}.txt"
        p.write_text(part + "\n", encoding="utf-8")
        written.append(p)

    print(f"OK: {len(written)} Datei(en) erzeugt.")
    print(f"- Titel erkannt: {raw_title}")
    print(f"- Präfix: {prefix}")
    print(f"- Gesamtdatei: {out_single}")
    for p in written:
        print(f"  * {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

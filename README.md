# 🎬 YouTube Transcript Exporter

Ein praktisches Python-Toolset, um **YouTube-Transkripte** automatisiert auszulesen, zu bereinigen und als Textdateien zu exportieren.  
Es unterstützt sowohl den **direkten Abruf über die YouTube-API** (via `youtube-transcript-api`) als auch das **lokale Extrahieren aus HTML-Dateien**, die du aus dem Browser exportierst.

---

## 📦 Installation

### 1. Repository klonen
```bash
git clone https://github.com/<dein-user>/py_yt_exporter.git
cd py_yt_exporter
```

### 2. Virtuelle Umgebung erstellen und aktivieren
```bash
python3 -m venv .venv_py_yt_html_extractor
. .venv_py_yt_html_extractor/bin/activate
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

---

## ⚙️ Dateien im Projekt

| Datei | Beschreibung |
|-------|---------------|
| `yt_text_extractor.py` | Holt Transkripte direkt über die YouTube-API (Online-Abruf). |
| `extract_from_html.py` | Extrahiert Transkripte aus lokal gespeicherten HTML-Dateien (Offline-Variante). |
| `combine.sh` | Bash-Skript zum automatischen Zusammenführen aller erzeugten Chunks. |
| `requirements.txt` | Liste der benötigten Python-Pakete. |
| `.gitignore` | Ignoriert Cache-Dateien, venv, Output-Dateien usw. |

---

## ▶️ Nutzung

### 1. Variante A – Online-Abruf über YouTube API

Extrahiert Transkripte direkt von YouTube (öffentliche Videos mit Transkript).  
Erfordert Internetverbindung und installiertes Paket `youtube-transcript-api`.

```bash
python yt_text_extractor.py --yt "https://www.youtube.com/watch?v=<VIDEO_ID>" --lang de
```

#### Beispiele

```bash
# Standard (deutsch bevorzugt)
python yt_text_extractor.py --yt "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --lang de

# Fallback auf Englisch erlauben
python yt_text_extractor.py --yt "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --lang de,en

# Mit Zeitstempeln behalten
python yt_text_extractor.py --yt "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --keep-timestamps
```

Ergebnis:
- `<video-title>_transcript.txt`
- `<video-title>_part_001.txt`, `_part_002.txt`, …

---

### 2. Variante B – Offline-Extraktion aus lokalem HTML

Wenn YouTube kein direktes API-Transkript liefert oder du offline arbeiten willst:  
1. Öffne das Video → Menü → **„Transkript anzeigen“**  
2. Rechtsklick → **„Seitenquelltext anzeigen“**  
3. Kompletten HTML-Code speichern, z. B. `transkript.html`

Dann:
```bash
python extract_from_html.py /pfad/zum/transkript.html
```

Das Skript:
- Findet automatisch alle Transkript-Segmente (`.segment-text`)  
- Bereinigt Zeitstempel und [Music]/[Applause]-Hinweise  
- Erstellt automatisch:
  - `<Titel>_transcript.txt`  
  - `<Titel>_part_001.txt`, `<Titel>_part_002.txt`, …

Exportiert wird standardmäßig **in denselben Ordner** wie die HTML-Datei.  
Optional kannst du einen anderen Zielpfad mit `--out-dir` angeben.

#### Beispiele

```bash
# Standard – alles bereinigt
python extract_from_html.py mein_video.html

# Zeitstempel behalten
python extract_from_html.py mein_video.html --keep-timestamps

# Cues ([Music], [Applause]) behalten
python extract_from_html.py mein_video.html --keep-cues
```

---

### 3. Chunks zusammenführen

Mitgeliefertes Bash-Skript `combine.sh`:
```bash
chmod +x combine.sh
./combine.sh <prefix>
```

Beispiel:
```bash
./combine.sh meinvideo
# Ergebnis: meinvideo_complete.txt
```

---

## 💡 Hinweise

- Nicht jedes Video hat ein maschinenlesbares Transkript.  
- Die API-Variante kann nur **öffentliche Videos** abrufen.  
- HTML-Variante funktioniert auch offline, solange der Transkript-Code sichtbar ist.  
- Chunks sind standardmäßig 12 000 Zeichen groß mit 500 Zeichen Überlappung (vermeidbarer Kontextverlust).

---

## 🧩 Anforderungen

```txt
beautifulsoup4>=4.12.0
lxml>=4.9.0
youtube-transcript-api==0.6.2
langdetect>=1.0.9   # optional
```

---

## 📜 Lizenz

MIT License © 2025 – frei verwendbar für private & kommerzielle Projekte.
````

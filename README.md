# 🎬 YouTube Transcript Exporter

Ein praktisches Python-Toolset, um **YouTube-Transkripte** automatisiert auszulesen, zu bereinigen und als Textdateien zu exportieren.  
Es unterstützt sowohl den **direkten Abruf über die YouTube-API** (via `youtube-transcript-api`) als auch das **lokale Extrahieren aus HTML-Dateien**, die du aus dem Browser exportierst.

---

## 📦 Installation

### 1. Repository klonen
```bash
git clone https://github.com/<dein-user>/py_yt_html_extractor.git
cd py_yt_html_extractor
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
| `py_yt_html_extractor.py` | Extrahiert Transkripte aus lokal gespeicherten HTML-Dateien (Offline-Variante). |
| `combine.sh` | Bash-Skript zum automatischen Zusammenführen aller erzeugten Chunks. |
| `requirements.txt` | Liste der benötigten Python-Pakete. |
| `.gitignore` | Ignoriert Cache-Dateien, venv, Output-Dateien usw. |

---

## ▶️ Nutzung

### Offline-Extraktion aus lokalem HTML

Wenn YouTube kein direktes API-Transkript liefert oder du offline arbeiten willst:  
1. Öffne das Video → Menü → **„Transkript anzeigen“**  
2. Rechtsklick → **„Seitenquelltext anzeigen“**  
3. Kompletten HTML-Code speichern, z. B. `transkript.html`

Dann:
```bash
python py_yt_html_extractor.py /pfad/zum/transkript.html
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
python py_yt_html_extractor.py mein_video.html

# Zeitstempel behalten
python py_yt_html_extractor.py mein_video.html --keep-timestamps

# Cues ([Music], [Applause]) behalten
python py_yt_html_extractor.py mein_video.html --keep-cues
```

---

### Chunks zusammenführen

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
- HTML-Variante funktioniert auch offline, solange der Transkript-Code sichtbar ist.  
- Chunks sind standardmäßig 12 000 Zeichen groß mit 500 Zeichen Überlappung (vermeidbarer Kontextverlust).

---

## 🧩 Anforderungen

```txt
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

---

## 📜 Lizenz

MIT License © 2025 – frei verwendbar für private & kommerzielle Projekte.

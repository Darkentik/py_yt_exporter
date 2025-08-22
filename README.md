# 🎬 YouTube Transcript Extractor

Ein CLI-Tool in **Python 3.10+**, das:

- YouTube-Transkripte **online** per [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/) lädt **oder**
- Transkripte aus **lokalem/rohem YouTube-HTML** extrahiert,
- den Text **säubert** (Zeitstempel, Sprecher, Cues entfernen – per Flags änderbar),
- und den Output in **Textdateien (Chunks)** schreibt, optimiert für ChatGPT.

---

## 📦 Installation

```bash
git clone https://github.com/<dein-user>/yt-text-extractor.git
cd yt-text-extractor

python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

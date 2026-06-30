import os
import httpx
from typing import Optional
from models.data import NoteInfo


DOWNLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "downloads"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.xiaohongshu.com/",
}


def download_file(url: str, filename: str, timeout: int = 120) -> Optional[str]:
    """Download a file from URL. Returns local file path or None."""
    if not url:
        return None
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    try:
        with httpx.stream(
            "GET", url, headers=HEADERS, follow_redirects=True, timeout=timeout
        ) as resp:
            if resp.status_code != 200:
                return None
            with open(filepath, "wb") as f:
                for chunk in resp.iter_bytes(chunk_size=8192):
                    f.write(chunk)
        if os.path.getsize(filepath) < 100:
            os.remove(filepath)
            return None
        return filepath
    except Exception as e:
        print(f"[Download] Error downloading {url[:80]}: {e}")
        return None


def download_note_media(note: NoteInfo) -> dict:
    """Download cover / video / images for a NoteInfo. Returns local paths."""
    nid = note.note_id
    paths = {"cover": None, "video": None, "images": []}

    if note.cover_url:
        paths["cover"] = download_file(note.cover_url, f"{nid}_cover.jpg")

    if note.video_url:
        paths["video"] = download_file(note.video_url, f"{nid}_video.mp4", timeout=180)

    if note.image_urls:
        for i, url in enumerate(note.image_urls.split(",")):
            url = url.strip()
            if url:
                p = download_file(url, f"{nid}_img_{i}.jpg")
                if p:
                    paths["images"].append(p)

    return paths


def cleanup_downloads():
    if os.path.exists(DOWNLOAD_DIR):
        for f in os.listdir(DOWNLOAD_DIR):
            try:
                os.remove(os.path.join(DOWNLOAD_DIR, f))
            except Exception:
                pass

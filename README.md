# 🎬 Video Player & Metadata Reader

A simple, mobile-friendly Streamlit app to upload a video, play it, and view its metadata (resolution, duration, codec, file size, and more) — all with a clean, modular Python structure.

## Features

- 📱 Mobile-friendly upload (works from phone browsers too)
- ▶️ In-browser video playback
- 📋 On-demand metadata display (tap "Show Metadata" — nothing loads until you ask)
- 🧩 Modular code — UI, metadata logic, and helpers are in separate files

## Project Structure

```
video-metadata-reader/
├── app.py                  # Streamlit UI (upload, player, button)
├── metadata_extractor.py   # Extracts metadata using OpenCV
├── utils.py                # File saving + formatting helpers
├── requirements.txt        # Python dependencies
└── README.md
```

## Metadata Fields Shown

| Field         | Description                                              |
|---------------|-----------------------------------------------------------|
| Title         | Original file name (without extension)                    |
| File Name     | Original uploaded file name                                |
| Server Path   | Temp path where the file is stored on the server            |
| Processed At  | Timestamp when the file was uploaded/processed              |
| Resolution    | Video width x height                                        |
| Duration      | Video length (HH:MM:SS or MM:SS)                             |
| FPS           | Frames per second                                            |
| Frame Count   | Total number of frames                                       |
| Codec         | Video codec (e.g. avc1, mp4v)                                 |
| File Size     | File size in MB/GB                                            |

> **Note:** Browsers don't share a file's original device metadata (its real creation/download time or its original phone file path) with web apps for privacy/security reasons. So "Server Path" and "Processed At" reflect the server side, not the original device — this app can't retrieve the exact original download time.

## Installation

```bash
git clone <your-repo-url>
cd video-metadata-reader
pip install -r requirements.txt
```

## Usage

Run locally:

```bash
streamlit run app.py
```

Run and access from your phone (same Wi-Fi network):

```bash
streamlit run app.py --server.address 0.0.0.0
```

Then open `http://<your-computer-local-ip>:8501` on your phone's browser.

## Requirements

- Python 3.8+
- streamlit
- opencv-python

(see `requirements.txt`)

## How It Works

1. User uploads a video via `st.file_uploader`.
2. The file is saved to a temporary path on the server (`utils.save_uploaded_file`), since OpenCV needs an actual file path, not just raw bytes.
3. The video plays inline using `st.video`.
4. On clicking **Show Metadata**, `metadata_extractor.get_video_metadata` opens the file with `cv2.VideoCapture` and reads its properties.
5. Metadata is displayed in a table.

## Possible Next Steps

- Add audio metadata (bitrate, audio codec) via `ffprobe`
- Add a cleanup/delete button to remove temp files from the server
- Support extracting a thumbnail preview frame

## License

Free to use and modify for personal or academic projects.
"""
utils.py
Helper functions: saving uploaded files to disk and formatting values
for display (bytes -> MB, seconds -> mm:ss, etc).
"""

import os
import tempfile
from datetime import datetime


def save_uploaded_file(uploaded_file, progress_callback=None) -> str:
    """
    Streamlit's file_uploader gives us an in-memory file object, not a
    real path on disk. cv2.VideoCapture needs an actual file path, so
    we write the bytes to a temp file once and reuse that path everywhere.

    Note: by the time this function runs, the browser -> server upload
    is already finished (Streamlit handles that internally, with its own
    built-in progress indicator on the widget itself — there's no way to
    hook into that part from our code). What we CAN show real progress
    for is this disk-write step, which is done in chunks below and is
    genuinely slow for large video files, especially on limited hosting.

    progress_callback: optional function called with a float 0.0-1.0
    as each chunk is written, so the UI can update a progress bar.
    """
    suffix = os.path.splitext(uploaded_file.name)[1] or ".mp4"
    total_size = uploaded_file.size
    chunk_size = 1024 * 1024  # 1 MB per chunk

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    written = 0

    uploaded_file.seek(0)
    while True:
        chunk = uploaded_file.read(chunk_size)
        if not chunk:
            break
        tfile.write(chunk)
        written += len(chunk)
        if progress_callback and total_size:
            progress_callback(min(written / total_size, 1.0))

    tfile.close()
    return tfile.name


def format_bytes(size_bytes: int) -> str:
    """Convert raw byte count into a human-readable MB/GB string."""
    mb = size_bytes / (1024 * 1024)
    if mb >= 1024:
        return f"{mb / 1024:.2f} GB"
    return f"{mb:.2f} MB"


def format_duration(seconds: float) -> str:
    """Convert seconds into HH:MM:SS (or MM:SS if under an hour)."""
    seconds = int(seconds)
    hrs, rem = divmod(seconds, 3600)
    mins, secs = divmod(rem, 60)
    if hrs:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def current_timestamp() -> str:
    """Timestamp for when the file was processed (upload time), not the
    original device's download/creation time — browsers don't expose that."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
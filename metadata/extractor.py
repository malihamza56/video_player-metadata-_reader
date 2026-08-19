"""
metadata_extractor.py
Pulls technical metadata out of a video file using OpenCV.
Kept separate from app.py so this logic can be reused or tested
without touching any Streamlit code.
"""

import os
import cv2

from utils.utils import format_bytes, format_duration, current_timestamp


def _decode_fourcc(fourcc_int: int) -> str:
    """
    OpenCV packs the 4-character codec code (e.g. 'avc1', 'mp4v')
    into a single float. Each of the 4 letters lives in one byte of
    a 32-bit number. Shifting right by 0/8/16/24 bits and masking
    with 0xFF pulls each byte out, then chr() turns it back into a
    letter.
    """
    return "".join([chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4)])


def get_video_metadata(path: str, original_filename: str) -> dict | None:
    """
    Opens the video at `path` and returns a dict of useful metadata.
    Returns None if the file can't be opened (corrupt/unsupported format).
    """
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
    duration_sec = frame_count / fps if fps > 0 else 0

    cap.release()

    title = os.path.splitext(original_filename)[0]

    return {
        "Title": title,
        "File Name": original_filename,
        "Server Path": path,  # server-side temp path, not the phone's original path
        "Processed At": current_timestamp(),
        "Resolution": f"{width} x {height}",
        "Duration": format_duration(duration_sec),
        "FPS": round(fps, 2),
        "Frame Count": int(frame_count),
        "Codec": _decode_fourcc(fourcc_int),
        "File Size": format_bytes(os.path.getsize(path)),
    }
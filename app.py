"""
app.py
Streamlit UI: upload a video (works from mobile browsers too),
play it, and reveal metadata only when the user taps "Show Metadata".
"""

import streamlit as st

from utils.utils import save_uploaded_file
from metadata.extractor import get_video_metadata

st.set_page_config(page_title="Video Player & Metadata Reader", page_icon="🎬")

st.title("🎬 Video Player & Metadata Reader")
st.caption("Upload a video, then tap the button to reveal its metadata.")

# session_state keeps the saved path around between reruns — Streamlit
# reruns the whole script top-to-bottom on every interaction (like a
# button click), so without this we'd lose track of the saved file.
if "video_path" not in st.session_state:
    st.session_state.video_path = None
    st.session_state.original_name = None

uploaded_file = st.file_uploader(
    "Upload a video",
    type=["mp4", "mov", "avi", "mkv", "webm"],
)

if uploaded_file is not None:
    # Only re-save if it's a new/different file, to avoid rewriting
    # the temp file on every rerun.
    if st.session_state.original_name != uploaded_file.name:
        st.session_state.video_path = save_uploaded_file(uploaded_file)
        st.session_state.original_name = uploaded_file.name

if st.session_state.video_path:
    st.video(st.session_state.video_path)

    if st.button("Show Metadata", use_container_width=True):
        metadata = get_video_metadata(
            st.session_state.video_path,
            st.session_state.original_name,
        )
        if metadata:
            st.subheader("📋 Metadata")
            st.table(metadata)
        else:
            st.error("Could not read metadata from this video.")
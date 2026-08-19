"""YouTube audio import for source/reference audio fields.

Downloads the audio track of a YouTube video to a temporary WAV file so it
can be dropped into the existing ``src_audio``/``reference_audio``
``gr.Audio(type="filepath")`` components, reusing the same validation and
generation pipeline as a manual upload.
"""

import os
import tempfile

import gradio as gr
from yt_dlp import YoutubeDL

from acestep.ui.gradio.i18n import t


def download_youtube_audio_to_temp(url: str) -> str:
    """Download a YouTube video's audio track to a temporary WAV file.

    Args:
        url: YouTube video URL.

    Returns:
        str: Path to the downloaded ``.wav`` file.

    Raises:
        Exception: Propagates ``yt_dlp`` download/extraction errors (invalid
            URL, unavailable/private video, no audio track, missing ffmpeg).
    """

    tmpdir = tempfile.mkdtemp(prefix="youtube_audio_")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(tmpdir, "audio.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        # The default "web" client's stream URLs frequently come back 403 from
        # YouTube's signature/token checks (common from datacenter IPs, e.g.
        # Colab). The Android/iOS clients use a different extraction path that
        # isn't subject to the same check, so try them first.
        "extractor_args": {"youtube": {"player_client": ["android", "ios", "web"]}},
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)

    return os.path.join(tmpdir, "audio.wav")


def fetch_youtube_audio_for_field(url: str):
    """Download YouTube audio and produce a ``gr.Audio`` value update.

    Shared handler for both the source-audio and reference-audio "fetch from
    YouTube" buttons — the contract (URL string in, filepath update out) is
    identical for either target component.

    Args:
        url: YouTube video URL pasted by the user.

    Returns:
        ``gr.update(value=<temp_wav_path>)`` on success, or ``gr.skip()`` to
        leave the target audio component untouched on a missing URL or
        download failure.
    """

    if not url or not url.strip():
        gr.Warning(t("messages.youtube_url_missing"))
        return gr.skip()

    try:
        audio_path = download_youtube_audio_to_temp(url.strip())
    except Exception as exc:
        gr.Warning(t("messages.youtube_fetch_failed", error=str(exc)))
        return gr.skip()

    gr.Info(t("messages.youtube_fetch_success"))
    return gr.update(value=audio_path)

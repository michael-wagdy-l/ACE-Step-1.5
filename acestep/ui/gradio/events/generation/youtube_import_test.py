"""Unit tests for the YouTube audio import handler."""

import unittest
from unittest.mock import patch

from acestep.ui.gradio.events.generation.youtube_import import (
    fetch_youtube_audio_for_field,
)


class FetchYoutubeAudioForFieldTests(unittest.TestCase):
    """Validate the shared fetch handler's success/failure contracts."""

    def test_blank_url_skips_without_downloading(self):
        with patch(
            "acestep.ui.gradio.events.generation.youtube_import.download_youtube_audio_to_temp"
        ) as mock_download:
            fetch_youtube_audio_for_field("   ")
        mock_download.assert_not_called()

    def test_download_failure_does_not_raise(self):
        with patch(
            "acestep.ui.gradio.events.generation.youtube_import.download_youtube_audio_to_temp",
            side_effect=RuntimeError("video unavailable"),
        ):
            fetch_youtube_audio_for_field("https://youtu.be/does-not-exist")

    def test_success_returns_value_update(self):
        with patch(
            "acestep.ui.gradio.events.generation.youtube_import.download_youtube_audio_to_temp",
            return_value="/tmp/audio.wav",
        ):
            result = fetch_youtube_audio_for_field("https://youtu.be/valid")
        self.assertEqual(result.get("value"), "/tmp/audio.wav")


if __name__ == "__main__":
    unittest.main()

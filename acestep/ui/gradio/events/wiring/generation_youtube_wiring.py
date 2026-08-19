"""Wiring for the "fetch audio from YouTube" buttons on the generation tab."""

from .. import generation_handlers as gen_h
from .context import GenerationWiringContext


def register_generation_youtube_handlers(context: GenerationWiringContext) -> None:
    """Wire the source/reference "fetch from YouTube" buttons.

    Downloads the pasted URL's audio to a temp file and drops it into the
    same ``src_audio``/``reference_audio`` components a manual upload would
    populate, re-triggering their existing ``.change`` validation.
    """

    generation_section = context.generation_section

    generation_section["fetch_youtube_src_btn"].click(
        fn=lambda url: gen_h.fetch_youtube_audio_for_field(url),
        inputs=[generation_section["youtube_url_src"]],
        outputs=[generation_section["src_audio"]],
    )

    generation_section["fetch_youtube_ref_btn"].click(
        fn=lambda url: gen_h.fetch_youtube_audio_for_field(url),
        inputs=[generation_section["youtube_url_ref"]],
        outputs=[generation_section["reference_audio"]],
    )

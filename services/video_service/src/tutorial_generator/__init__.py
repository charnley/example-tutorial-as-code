import logging
from pathlib import Path

from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
from tutorial_generator.video_funcs import generate_video
from tutorial_generator.speech_funcs import generate_audio
from tutorial_generator.section import SectionList

from .constants import DEFAULT_VIEWPOINT_WIDTH, DEFAULT_VIEWPOINT_HEIGHT

logger = logging.getLogger(__name__)

def synchronize_video_audio(video_filename, audio_filenames, timestamps):

    video = VideoFileClip(str(video_filename))

    audio_clips = []

    for audio_path, timestamp in zip(audio_filenames, timestamps):
        audio = AudioFileClip(str(audio_path))
        audio_clips.append(audio.with_start(timestamp))

    # Composite audio and apply to video
    final_audio = CompositeAudioClip(audio_clips)
    final_video = video.with_audio(final_audio)

    return final_video


def trim_video(video: VideoFileClip, start_time: float) -> VideoFileClip:
    """Trim video to start from specified time."""
    assert start_time < video.duration
    return video.subclipped(start_time)


def save_video(video: VideoFileClip, filename):

    is_webm = filename.suffix.lower() == '.webm'
    audio_codec = "libvorbis" if is_webm else "aac"

    video.write_videofile(str(filename), audio_codec=audio_codec)


def generate_tutorial(name, voice, actions, texts, remove_first_section=False, browser_width=DEFAULT_VIEWPOINT_WIDTH, browser_height=DEFAULT_VIEWPOINT_HEIGHT):

    logger.info(f"Generating {name} tutorial")

    tmp_dir = Path("tmp_videos")
    video_name = f"{name}"

    assert len(actions) == len(texts)

    logger.info(f"Generating audio files")

    audio_filenames = []

    for i, text in enumerate(texts):

        if text is None:
            audio_filenames.append(None)
            logger.info(f"Section {i} has no audio, skipping")
            continue

        filename = tmp_dir / f"section_{i}"
        filename = generate_audio(voice, text, filename)
        audio_filenames.append(filename)

        logger.info(f"Finished {filename}")

    # Compute audio durations so generate_video can pause after each section
    # to prevent narration from overlapping with the next section.
    # Sections with no audio (None) get duration 0.
    audio_durations = [
        AudioFileClip(str(f)).duration if f is not None else 0.0
        for f in audio_filenames
    ]

    logger.info(f"Generating video file")

    timestamps = generate_video(Path(video_name), actions, browser_width=browser_width, browser_height=browser_height, audio_durations=audio_durations)

    timestamps = [0] + timestamps[:-1]

    video_filename = tmp_dir / Path(video_name).with_suffix(".webm")

    logger.info(f"Adding audio to video")

    # Only pass sections that actually have audio to synchronize_video_audio
    audio_pairs = [(f, t) for f, t in zip(audio_filenames, timestamps) if f is not None]
    if audio_pairs:
        active_filenames, active_timestamps = zip(*audio_pairs)
        video = synchronize_video_audio(video_filename, active_filenames, active_timestamps)
    else:
        video = VideoFileClip(str(video_filename))

    if remove_first_section:

        assert len(timestamps) > 1, "what do you want to remove? only 1 section"

        logger.info(f"Trimming video to start at section 2 (timestamp: {timestamps[1]})")
        video = trim_video(video, timestamps[1])

    logger.info(f"Saving video")
    output_path = video_filename.parent / f"{video_filename.stem}_merged{video_filename.suffix}"
    save_video(video, output_path)

    return True

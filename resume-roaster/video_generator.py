"""
Video generation module for Resume Roaster
Converts roast text to speech and creates a video with visuals
"""

import os
from pathlib import Path
from typing import Optional
import json

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("Warning: gTTS not installed. Install with: pip install gtts")

try:
    from moviepy import (
        ImageClip, AudioFileClip, TextClip, CompositeVideoClip,
        concatenate_videoclips, ColorClip, VideoFileClip
    )
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("Warning: moviepy not installed. Install with: pip install moviepy")

# Path to background videos
VIDEOS_DIR = Path(__file__).parent.parent / "videos"

# Available background videos
BACKGROUND_VIDEOS = {
    "subway_surfer": "subway_surfer.mp4",
    "minecraft": "minecraft.mp4",
    "fortnite": "fortnite.mp4",
    "templerun": "templerun.mp4",
    "satisfying": "satisfying.mp4"
}


def generate_video(
    roast_text: str,
    score: int,
    output_path: str,
    issues: list = None,
    tone: str = "medium",
    background_video: str = "subway_surfer"
) -> str:
    """
    Generate a brainrot-style video from roast text with gameplay background

    Args:
        roast_text: The roast content to convert to speech
        score: Resume score (0-100)
        output_path: Path where video should be saved
        issues: List of issues found in resume
        tone: Roast tone (gentle, medium, savage)
        background_video: Background video type (subway_surfer, minecraft, fortnite, templerun, satisfying)

    Returns:
        Path to generated video file
    """
    if not GTTS_AVAILABLE or not MOVIEPY_AVAILABLE:
        # Create a simple placeholder video with text
        return create_placeholder_video(roast_text, score, output_path)

    try:
        # Step 1: Generate speech from text
        audio_path = output_path.replace('.mp4', '_audio.mp3')
        tts = gTTS(text=roast_text, lang='en', slow=False)
        tts.save(audio_path)

        # Step 2: Load audio to get duration
        audio = AudioFileClip(audio_path)
        duration = audio.duration

        # Step 3: Create video visuals with background
        video = create_video_visuals(roast_text, score, duration, tone, issues, background_video)

        # Step 4: Combine audio and video
        final_video = video.set_audio(audio)

        # Step 5: Export video
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=output_path.replace('.mp4', '_temp_audio.m4a'),
            remove_temp=True
        )

        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)

        audio.close()
        video.close()
        final_video.close()

        return output_path

    except Exception as e:
        print(f"Error generating video: {e}")
        return create_placeholder_video(roast_text, score, output_path)


def create_video_visuals(
    roast_text: str,
    score: int,
    duration: float,
    tone: str,
    issues: list = None,
    background_video: str = "subway_surfer"
) -> CompositeVideoClip:
    """
    Create brainrot-style video visuals with gameplay background and text overlay
    """
    # Video dimensions for portrait mode (brainrot style)
    width, height = 1080, 1920

    # Load background video
    bg_video_filename = BACKGROUND_VIDEOS.get(background_video, BACKGROUND_VIDEOS["subway_surfer"])
    bg_video_path = VIDEOS_DIR / bg_video_filename

    if not bg_video_path.exists():
        print(f"Warning: Background video not found at {bg_video_path}, using colored background")
        # Fallback to colored background
        if score >= 80:
            bg_color = (34, 139, 34)  # Green
        elif score >= 60:
            bg_color = (255, 165, 0)  # Orange
        else:
            bg_color = (220, 20, 60)  # Red

        background = ColorClip(
            size=(width, height),
            color=bg_color,
            duration=duration
        )
    else:
        # Load and loop the background video
        background = VideoFileClip(str(bg_video_path))

        # Loop background video if roast is longer than background
        if background.duration < duration:
            num_loops = int(duration / background.duration) + 1
            background = concatenate_videoclips([background] * num_loops)

        # Trim to match audio duration using subclipped method
        if hasattr(background, 'subclipped'):
            background = background.subclipped(0, duration)
        elif hasattr(background, 'subclip'):
            background = background.subclip(0, duration)
        else:
            # For newer moviepy versions, use set_duration
            background = background.with_duration(duration)

        # Resize to fit portrait mode if needed
        if hasattr(background, 'resized'):
            background = background.resized(height=height)
        else:
            background = background.resize(height=height)

    # Create title with stroke for better visibility
    title_text = f"Resume Roast\nScore: {score}/100"
    try:
        title = TextClip(
            text=title_text,
            font_size=60,
            color='white',
            font='Arial-Bold',
            size=(width - 100, None),
            method='caption',
            text_align='center',
            stroke_color='black',
            stroke_width=3
        )
        if hasattr(title, 'with_position'):
            title = title.with_position(('center', 100)).with_duration(duration)
        else:
            title = title.set_position(('center', 100)).set_duration(duration)
    except Exception as e:
        print(f"Error creating title: {e}")
        # Skip title if there's an error
        title = None

    # Split roast text into smaller chunks for TikTok-style text
    words_per_chunk = 15  # Smaller chunks for better readability
    words = roast_text.split()
    chunks = []

    for i in range(0, len(words), words_per_chunk):
        chunk = ' '.join(words[i:i + words_per_chunk])
        chunks.append(chunk)

    # Calculate time per chunk
    chunk_duration = duration / len(chunks) if chunks else duration

    # Create text clips for each chunk (centered on screen, brainrot style)
    text_clips = []
    for i, chunk in enumerate(chunks):
        try:
            text_clip = TextClip(
                text=chunk,
                font_size=50,
                color='yellow',
                font='Arial-Bold',
                size=(width - 100, None),
                method='caption',
                text_align='center',
                stroke_color='black',
                stroke_width=4
            )
            if hasattr(text_clip, 'with_position'):
                text_clip = text_clip.with_position(('center', 'center')).with_start(i * chunk_duration).with_duration(chunk_duration)
            else:
                text_clip = text_clip.set_position(('center', 'center')).set_start(i * chunk_duration).set_duration(chunk_duration)
            text_clips.append(text_clip)
        except Exception as e:
            print(f"Error creating text clip {i}: {e}")
            continue

    # Combine all elements
    clips_to_composite = [background]
    if title:
        clips_to_composite.append(title)
    clips_to_composite.extend(text_clips)

    video = CompositeVideoClip(clips_to_composite, size=(width, height))

    return video


def create_placeholder_video(roast_text: str, score: int, output_path: str) -> str:
    """
    Create a simple placeholder when video generation dependencies are not available
    Creates a basic MP4 file with metadata
    """
    try:
        # Create a minimal valid MP4 file structure
        # This is a hack - in production you'd want proper video generation

        # For now, save the roast as a JSON file alongside
        json_path = output_path.replace('.mp4', '_data.json')
        with open(json_path, 'w') as f:
            json.dump({
                'roast_text': roast_text,
                'score': score,
                'note': 'Install gTTS and moviepy for actual video generation'
            }, f, indent=2)

        # Create a minimal MP4 file (this won't be playable, but it's a placeholder)
        # In a real scenario, you'd use actual video generation
        with open(output_path, 'wb') as f:
            # Write minimal MP4 header (not a valid video, just a placeholder)
            f.write(b'\x00\x00\x00\x20ftypisom\x00\x00\x02\x00isomiso2mp41')

        print(f"Created placeholder video at {output_path}")
        print(f"Install dependencies for real videos: pip install gtts moviepy")

        return output_path

    except Exception as e:
        print(f"Error creating placeholder: {e}")
        return output_path


def get_video_dependencies_status() -> dict:
    """
    Check if video generation dependencies are installed
    """
    return {
        'gtts': GTTS_AVAILABLE,
        'moviepy': MOVIEPY_AVAILABLE,
        'ready': GTTS_AVAILABLE and MOVIEPY_AVAILABLE
    }


def get_available_backgrounds() -> list:
    """
    Get list of available background videos
    """
    return list(BACKGROUND_VIDEOS.keys())


if __name__ == "__main__":
    # Test video generation
    test_roast = """
    Alright, let's talk about this resume. First off, using 'ishaankalra@gmail.com' as your
    professional email? Come on! You're not applying to be your mom's favorite developer.
    Get a professional email address!

    Your experience section is full of buzzwords like 'synergy' and 'innovative' - these words
    mean absolutely nothing. Show me NUMBERS! How many users? How much did you improve performance?

    And what's with all these weak verbs? 'Helped with', 'Worked on', 'Participated in' - you
    sound like you were just standing around watching people work. Use strong action verbs!

    But hey, at least you spelled everything correctly. That's more than I can say for most
    resumes I've seen. Overall score: 65/100. You've got potential, but this resume needs work!
    """

    status = get_video_dependencies_status()
    print(f"Video generation dependencies: {status}")

    if status['ready']:
        output = "test_roast.mp4"
        generate_video(test_roast, 65, output, tone="medium")
        print(f"Test video generated: {output}")
    else:
        print("Install dependencies to test: pip install gtts moviepy")

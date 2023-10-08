from pydub import AudioSegment
import numpy as np
import os
from moviepy.editor import VideoFileClip
from space_audio_without_gui_copy1 import process_img
from PIL import Image

# Video file input path
video_path = 'FlighttoAGCarinae.mp4'  # Replace with your video file path

# Desired frame rate (1 frame per second)
frame_rate = 1

# Load the video clip
video_clip = VideoFileClip(video_path)

# Create a directory to store processed frames as images
output_dir = 'processed_frames'
os.makedirs(output_dir, exist_ok=True)

# Process frames that occur every 1 second in the video
audio_segments = []

frame_counter = 0  # Initialize frame counter
for i, frame in enumerate(video_clip.iter_frames(fps=video_clip.fps)):
    # Check if it's time to process a frame
    if i >= frame_counter:
        # Save the frame as an image
        frame_image_path = os.path.join(output_dir, f'frame_{i:04d}.jpg')
        Image.fromarray(frame).save(frame_image_path)

        # Process the saved image and get the audio segment
        audio_segment = AudioSegment(data=process_img(frame_image_path), sample_width=2, frame_rate=44100, channels=1)
        audio_segments.append(audio_segment)

        # Increment the frame counter to the next second
        frame_counter += video_clip.fps

# Combine the audio segments into a single audio file using overlay method
combined_audio = audio_segments[0]
for audio_segment in audio_segments[1:]:
    combined_audio = combined_audio.overlay(audio_segment)

# Export the combined audio as an audio file (e.g., WAV or MP3)
output_audio_path = 'output_audio.mp3'  # Replace with your desired output audio file path
combined_audio.export(output_audio_path, format='mp3')

print(f"Combined audio saved as '{output_audio_path}'")

from pydub import AudioSegment
import numpy as np
import os
from moviepy.editor import VideoFileClip
from space_audio_without_gui_copy import process_img
from PIL import Image

# Video file input path
video_path = 'FlighttoAGCarinae.mp4'  # Replace with your video file path

# Load the video clip
video_clip = VideoFileClip(video_path)

# Create a directory to store processed frames as images
output_dir = 'processed_frames'
os.makedirs(output_dir, exist_ok=True)

# Process each frame in the video and collect audio segments
audio_segments = []

for i, frame in enumerate(video_clip.iter_frames()):
    # Save the frame as an image
    frame_image_path = os.path.join(output_dir, f'frame_{i:04d}.jpg')
    Image.fromarray(frame).save(frame_image_path)

    # Process the saved image and get the audio segment
    audio_segment = AudioSegment(data=process_img(frame_image_path), sample_width=2, frame_rate=44100, channels=1)
    audio_segments.append(audio_segment)

# Combine the audio segments into a single audio file
combined_audio = sum(audio_segments)

# Export the combined audio as an audio file (e.g., WAV or MP3)
output_audio_path = 'output_audio.mp3'  # Replace with your desired output audio file path
combined_audio.export(output_audio_path, format='mp3')

print(f"Combined audio saved as '{output_audio_path}'")

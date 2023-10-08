import os
from moviepy.editor import VideoFileClip
from space_audio_without_gui_copy1 import process_img
from PIL import Image
import soundfile as sf
import numpy as np

# Video file input path
video_path = 'first_seconds.mp4'  # Replace with your video file path

# Desired frame rate (1 frame per second)
frame_rate = 1

# Define the sample rate for the audio segments
sample_rate = 44100  # Adjust as needed based on your requirements

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
        audio_segment = process_img(frame_image_path)
        audio_segments.extend(audio_segment)  # Extend the list with audio data segments

        # Increment the frame counter to the next second
        frame_counter += video_clip.fps


with sf.SoundFile('space_audio_grouped5.wav', 'w', sample_rate, 1) as file:
    for audio_data in audio_segments:
        file.write(audio_data)
'''
# Convert the concatenated audio segments to a NumPy array
audio_data = np.concatenate(audio_segments)

# Export the audio data to a WAV file using soundfile
output_audio_path_wav = 'space_audio_grouped2.wav'
sf.write(output_audio_path_wav, audio_data, sample_rate)

print(f"Audio saved as '{output_audio_path_wav}'")

# Now, you have a single audio file for the entire video.'''

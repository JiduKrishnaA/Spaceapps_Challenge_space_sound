from moviepy.editor import VideoFileClip
from pydub import AudioSegment

# Load the video file
video_path = 'your_video.mp4'  # Replace with your video file path
video_clip = VideoFileClip(video_path)

# Create a sound clip (adjust the duration and audio parameters as needed)
sound_duration = video_clip.duration  # Use the video's duration
sound = AudioSegment.silent(duration=sound_duration * 1000)  # Duration in milliseconds

# Add sound to the video
video_clip = video_clip.set_audio(sound)

# Specify the output video file path
output_path = 'video_with_sound.mp4'  # Replace with your desired output file path

# Write the video with sound to a file
video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

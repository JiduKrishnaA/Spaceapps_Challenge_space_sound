from moviepy.editor import VideoFileClip

# Input video file path
video_path = 'FlighttoAGCarinae.mp4'  # Replace with your video file path

# Output video file path for the first 2 seconds
output_path = 'first_seconds.mp4'  # Replace with your desired output video file path

# Load the video clip
video_clip = VideoFileClip(video_path)

# Extract the first 2 seconds of the video
first_2_seconds_clip = video_clip.subclip(0, 1)

# Write the extracted clip to a new video file
first_2_seconds_clip.write_videofile(output_path, codec='libx264')

print(f"First 2 seconds of the video saved as '{output_path}'")

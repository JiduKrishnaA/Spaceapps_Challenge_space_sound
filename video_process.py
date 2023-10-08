from moviepy.editor import VideoFileClip, clips_array
import os
from space_audio_without_gui_copy import process_img

# Video file input path
video_path = 'FlighttoAGCarinae.mp4'  # Replace with your video file path

# Create a directory to store processed frames
output_dir = 'processed_frames'
os.makedirs(output_dir, exist_ok=True)

# Function to process a single frame
def process_frame(frame):
    # Replace this with your image processing code
    # In this example, we'll just convert the frame to grayscale
    process_img(frame)
    #processed_frame = frame.to_grayscale()
    #return processed_frame

# Load the video clip
video_clip = VideoFileClip(video_path)

# Process each frame in the video
processed_frames = [process_frame(frame) for frame in video_clip.iter_frames()]

'''
# Save the processed frames as images (optional)
for i, frame in enumerate(processed_frames):
    frame_filename = os.path.join(output_dir, f'frame_{i:04d}.jpg')
    frame.save_frame(frame_filename)

# Combine the processed frames into a video
processed_video = clips_array([[frame] for frame in processed_frames])

# Write the processed video to an output file
output_video_path = 'output_video.mp4'  # Replace with your desired output video file path
processed_video.write_videofile(output_video_path, codec='libx264')

print(f"Processed frames saved in '{output_dir}'")
print(f"Output video saved as '{output_video_path}'")
'''

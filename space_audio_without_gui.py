from pydub import AudioSegment
import numpy as np
from PIL import Image
import soundfile as sf
import scipy.signal as signal
from brightest_point import find_brightest

def process_img(image_path):
    # Load the space image
    #image_path = 'M31_HubbleSpitzerGendler_2000.jpg'
    space_image = Image.open(image_path)

    # Convert the image to grayscale
    space_image_gray = space_image.convert('L')

    # Get pixel data as a NumPy array
    pixel_data = np.array(space_image_gray)

    # Load the bell sound
    bell_sound_path = 'bells.wav'
    bell_sound = AudioSegment.from_file(bell_sound_path, format="wav")
    bell_sound = bell_sound.set_channels(1)

    # Define parameters for audio generation
    sample_rate = 44100  # Sample rate in Hz
    duration = 0.48  # Duration of each audio segment in seconds (adjust as needed)

    # Map pixel brightness to audio frequencies
    def brightness_to_frequency(brightness):
        # You can adjust this mapping as needed
        min_brightness = 100
        max_brightness = 255
        min_frequency = 700  # Minimum frequency in Hz
        max_frequency = 1400  # Maximum frequency in Hz
        
        # Linear mapping from brightness to frequency
        return min_frequency + (max_frequency - min_frequency) * (brightness - min_brightness) / (max_brightness - min_brightness)

    # Initialize an empty audio array
    total_duration = 360  # Total duration in degrees (0 to 360)
    total_samples = int(sample_rate * total_duration)

    # Define the chunk size for incremental audio generation
    chunk_size = int(sample_rate * duration)

    # Initialize an empty audio array
    audio_data = np.zeros(chunk_size)

    # Initialize the initial phase of the waveform
    current_phase = 0.0

    # Get the center coordinates of the image
    #center_x, center_y = pixel_data.shape[1] // 2, pixel_data.shape[0] // 2

    ###
    #addition: find brightest point on image as center
    center_x,center_y=find_brightest(image_path)
    ###

    # Define the group size for accumulating brightness values
    group_size = 5  # Adjust the group size as needed

    # Generate audio and save it incrementally while rotating the line
    with sf.SoundFile('space_audio_grouped.wav', 'w', sample_rate, 1) as file:
        for angle_deg in range(0, 360):
            angle_rad = np.radians(angle_deg)
            
            # Calculate the endpoints of the line
            x1, y1 = center_x, center_y
            x2, y2 = (
                center_x + int(center_x * np.cos(angle_rad)),
                center_y + int(center_y * np.sin(angle_rad))
            )
            
            # Get the coordinates of all pixels along the line using Bresenham's algorithm
            line_pixels_x, line_pixels_y = [], []
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            x, y = x1, y1
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy
            
            while True:
                # Check if the coordinates are within bounds
                if 0 <= x < pixel_data.shape[1] and 0 <= y < pixel_data.shape[0]:
                    line_pixels_x.append(x)
                    line_pixels_y.append(y)
                
                if x == x2 and y == y2:
                    break
                
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x += sx
                if e2 < dx:
                    err += dx
                    y += sy
            
            # Group the pixels into batches and calculate the average brightness
            grouped_brightness = []
            for i in range(0, len(line_pixels_x), group_size):
                group_x = line_pixels_x[i:i+group_size]
                group_y = line_pixels_y[i:i+group_size]
                
                # Convert x and y coordinates to integers before accessing pixel values
                group_brightness = [pixel_data[int(y), int(x)] for x, y in zip(group_x, group_y)]
                average_brightness = np.mean(group_brightness)
                grouped_brightness.append(average_brightness)

            # Map average brightness to frequency
            frequencies = [brightness_to_frequency(brightness) for brightness in grouped_brightness]
            
            # Generate audio for each group
            for frequency in frequencies:
                t = np.linspace(0, duration, chunk_size, endpoint=False)
                waveform = np.sin(2 * np.pi * frequency * t + current_phase)
        
                fade_duration = 0.001  # Adjust the fade duration as needed
                fade_samples = int(fade_duration * sample_rate)
                envelope = np.ones(chunk_size)
                envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
                envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
                waveform *= envelope
        
                if average_brightness > 150:  # Adjust the threshold as needed
                    special_tune = np.array(bell_sound.get_array_of_samples())
                    waveform += special_tune[:chunk_size]

            audio_data += waveform
            
            # Update the phase for the next iteration to ensure continuity
            current_phase = (current_phase + 2 * np.pi * frequency * duration) % (2 * np.pi)
            
            # Check if it's time to save the audio data
            if angle_deg % 10 == 0:
                file.write(audio_data / np.max(np.abs(audio_data)))  # Normalize audio data
                audio_data = np.zeros(chunk_size)

    print("Grouped rotating line audio file 'space_audio_grouped.wav' has been generated.")

process_img('heic0506a.jpg')

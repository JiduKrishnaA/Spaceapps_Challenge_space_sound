import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pydub import AudioSegment
import numpy as np
import soundfile as sf
import pygame

# Define the GUI class
class ImageToAudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Audio Converter")
        
        # Initialize variables
        self.image_path = ""
        self.sound_path = ""
        self.audio_file = "space_audio_grouped.wav"  # Added a variable to store the audio file path
        
        # Set window resolution
        self.root.geometry("920x1080")
        self.root.configure(bg="grey")
        
        # Create labels
        self.image_label = tk.Label(root, text="Select Image:")
        self.sound_label = tk.Label(root, text="Select Sound:")
        
        # Create buttons to select files
        self.image_button = tk.Button(root, text="Browse Image", command=self.select_image)
        self.sound_button = tk.Button(root, text="Browse Sound", command=self.select_sound)
        
        # Create image preview area
        self.image_preview_label = tk.Label(root, text="Image Preview:")
        self.image_preview = tk.Label(root)
        self.ima_label = tk.Label(root, text="After uploading, wait for the audio to generate :)")
        
        # Create convert button
        self.convert_button = tk.Button(root, text="Convert", command=self.convert)
        
        # Create play button for audio
        self.play_button = tk.Button(root, text="Play Audio", command=self.play_audio)  # Added a play button
        
        # Place widgets on the grid
        self.image_label.grid(row=0, column=0, padx=10, pady=10)
        self.image_button.grid(row=0, column=1, padx=10, pady=10)
        self.sound_label.grid(row=1, column=0, padx=10, pady=10)
        self.sound_button.grid(row=1, column=1, padx=10, pady=10)
        self.image_preview_label.grid(row=2, columnspan=2, padx=10, pady=10)
        self.image_preview.grid(row=3, columnspan=2, padx=10, pady=10)
        self.ima_label.grid(row=4, columnspan=2, padx=10, pady=10)
        self.convert_button.grid(row=5, columnspan=2, padx=10, pady=10)
        self.play_button.grid(row=6, columnspan=2, padx=10, pady=10)  # Place the play button
        
        # Initialize pygame for audio playback
        pygame.init()
    
    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff")])
        if self.image_path:
            image = Image.open(self.image_path)
            image = ImageTk.PhotoImage(image)
            self.image_preview.config(image=image)
            self.image_preview.image = image
    
    def select_sound(self):
        self.sound_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
    
    def convert(self):
        if not self.image_path or not self.sound_path:
            messagebox.showerror("Error", "Please select both an image and a sound file.")
            return
        
        # Load the space image
        space_image = Image.open(self.image_path)
        space_image_gray = space_image.convert('L')
        pixel_data = np.array(space_image_gray)

        # Load the bell sound
        bell_sound = AudioSegment.from_file(self.sound_path, format="wav")
        bell_sound = bell_sound.set_channels(1)
        
        # Define parameters for audio generation
        sample_rate = 44100
        duration = 0.48
        
        # Initialize an empty audio array
        total_duration = 360
        total_samples = int(sample_rate * total_duration)
        chunk_size = int(sample_rate * duration)
        audio_data = np.zeros(chunk_size)
        current_phase = 0.0
        center_x, center_y = pixel_data.shape[1] // 2, pixel_data.shape[0] // 2
        group_size = 5

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
                    group_brightness = [pixel_data[y, x] for x, y in zip(group_x, group_y)]
                    average_brightness = np.mean(group_brightness)
                    grouped_brightness.append(average_brightness)
                
                # Map average brightness to frequency
                frequencies = [self.brightness_to_frequency(brightness) for brightness in grouped_brightness]
                
                # Generate audio for each group
                for frequency in frequencies:
                    t = np.linspace(0, duration, chunk_size, endpoint=False)
                    waveform = np.sin(2 * np.pi * frequency * t + current_phase)
            
                    fade_duration = 0.001
                    fade_samples = int(fade_duration * sample_rate)
                    envelope = np.ones(chunk_size)
                    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
                    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
                    waveform *= envelope
            
                    if average_brightness > 150:
                        special_tune = np.array(bell_sound.get_array_of_samples())
                        waveform += special_tune[:chunk_size]

                audio_data += waveform
                
                # Update the phase for the next iteration to ensure continuity
                current_phase = (current_phase + 2 * np.pi * frequency * duration) % (2 * np.pi)
                
                # Check if it's time to save the audio data
                if angle_deg % 10 == 0:
                    file.write(audio_data / np.max(np.abs(audio_data)))  # Normalize audio data
                    audio_data = np.zeros(chunk_size)
        
        messagebox.showinfo("Conversion Complete", "Audio conversion completed.")
        print("Grouped rotating line audio file 'space_audio_grouped.wav' has been generated.")
    
    def brightness_to_frequency(self, brightness):
        min_brightness = 100
        max_brightness = 255
        min_frequency = 700
        max_frequency = 1400
        return min_frequency + (max_frequency - min_frequency) * (brightness - min_brightness) / (max_brightness - min_brightness)

    def play_audio(self):
        if self.audio_file:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToAudioConverterApp(root)
    root.mainloop()

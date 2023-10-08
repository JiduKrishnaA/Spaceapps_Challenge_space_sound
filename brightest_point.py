# this code finds the approximate brightest point in an image
import numpy as np
from skimage import io, filters, morphology
from scipy.ndimage import label

# Load the galaxy image
image_path = 'heic0506a.jpg'  # Replace with your galaxy image file path
image = io.imread(image_path)

# Convert the image to grayscale
gray_image = np.mean(image, axis=2)

# Apply a threshold to segment the brightest regions
threshold = filters.threshold_otsu(gray_image)
binary_image = gray_image > threshold

# Clean up the binary image (optional)
binary_image = morphology.remove_small_objects(binary_image, min_size=100)

# Label connected components in the binary image
labeled_image, num_features = label(binary_image)

# Find the region with the largest area (brightest part of the galaxy)
largest_region = None
largest_area = 0

for region_label in range(1, num_features + 1):
    region_mask = labeled_image == region_label
    region_area = np.sum(region_mask)
    
    if region_area > largest_area:
        largest_area = region_area
        largest_region = region_mask

# Find the centroid of the largest region
centroid = np.argwhere(largest_region).mean(axis=0)

# Access coordinates of the brightest part of the galaxy
brightest_x, brightest_y = centroid

print(f'Brightest part of the galaxy: X={brightest_x}, Y={brightest_y}')



###
# Draw a marker (a red circle, for example) at the brightest hotspot
from PIL import ImageDraw, Image
image1 = Image.open(image_path)
# Create a copy of the original image to mark the hotspot
image_with_marker = image1.copy()

draw = ImageDraw.Draw(image_with_marker)
marker_radius = 5 # Adjust the marker size as needed
marker_color = (255, 0, 0)  # Red color (R, G, B)
draw.ellipse([(brightest_y - marker_radius, brightest_x - marker_radius),
                (brightest_y + marker_radius, brightest_x + marker_radius)],
                outline=marker_color, width=2)

# Display or save the image with the marker
image_with_marker.show()  # Display the image
# image_with_marker.save('image_with_marker.jpg')  # Save the image with the marker
####

# You can also mark the brightest part on the original image (optional)
#image[binary_image] = [255, 0, 0]  # Mark in red

# Display or save the marked image (optional)
#io.imshow(image)
#io.show()

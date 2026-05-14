# Import sys and os to manage file paths
import sys
import os

# Add the parent project folder to Python path
# This allows this test file to import modules from the processing folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import OpenCV for image creation, drawing, displaying, and image processing
import cv2

# Import NumPy to create blank image arrays
import numpy as np

# Import the DifferenceDetector class to detect differences between two images
from processing.difference_detector import DifferenceDetector


# Create a blank black image with size 400 x 400 and 3 colour channels
image_a = np.zeros((400, 400, 3), dtype=np.uint8)

# Create a copy of image_a to use as the modified image
image_b = image_a.copy()

# Draw a white filled rectangle on image_b to create a visible difference
cv2.rectangle(image_b, (100, 100), (250, 250), (255, 255, 255), -1)

# Create a DifferenceDetector object
# threshold controls how sensitive the detector is
# min_area ignores very small detected regions/noise
detector = DifferenceDetector(threshold=30, min_area=100)

# Detect the difference regions between image_a and image_b
regions = detector.detect(image_a, image_b)

# Print the total number of detected difference regions
print("Number of regions:", len(regions))

# Loop through each detected region
for region in regions:
    # Print region information as a dictionary
    print(region.to_dict())

    # Draw a rectangle around the detected region on image_b
    region.draw(image_b)

# Display the original image
cv2.imshow("Image A", image_a)

# Display the modified image with detected difference marked
cv2.imshow("Image B with Detected Difference", image_b)

# Keep the image windows open until any key is pressed
cv2.waitKey(0)

# Close all OpenCV image windows
cv2.destroyAllWindows()

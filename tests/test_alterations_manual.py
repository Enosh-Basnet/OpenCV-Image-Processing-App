# Import sys and os to manage file paths
import sys
import os

# Add the parent project folder to Python path
# This allows this test file to import modules from models and alterations folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import OpenCV for creating and processing test images
import cv2

# Import NumPy to create a blank image array
import numpy as np

# Import DifferenceRegion model class
from models.difference_region import DifferenceRegion

# Import different alteration classes
from alterations.colour_shift import ColourShift
from alterations.object_added import ObjectAdded
from alterations.object_removed import ObjectRemoved


# Create a blank black image with size 400 x 400 and 3 colour channels
image = np.zeros((400, 400, 3), dtype=np.uint8)

# Draw a white filled rectangle on the black image
cv2.rectangle(image, (100, 100), (250, 250), (255, 255, 255), -1)

# Convert the image from BGR colour format to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find contours from the grayscale image
# RETR_EXTERNAL gets only the outer contour
# CHAIN_APPROX_SIMPLE compresses contour points to save memory
contours, _ = cv2.findContours(
    gray,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

# Create a DifferenceRegion object using the first detected contour
region = DifferenceRegion(contours[0])

# Create different alteration objects using the same region
colour_shift = ColourShift(region)
object_added = ObjectAdded(region)
object_removed = ObjectRemoved(region)

# Print dictionary information for each alteration object
print(colour_shift.to_dict())
print(object_added.to_dict())
print(object_removed.to_dict())

# Test whether a point is inside the alteration region
print("Point inside:", colour_shift.contains_point(150, 150))

# Test whether a point is outside the alteration region
print("Point outside:", colour_shift.contains_point(300, 300))

# Mark the colour shift alteration as found
colour_shift.mark_found()

# Print alteration information again after marking it as found
print("After found:", colour_shift.to_dict())

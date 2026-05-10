import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import cv2
import numpy as np
from models.difference_region import DifferenceRegion


# Create blank image
image = np.zeros((400, 400, 3), dtype=np.uint8)

# Draw white rectangle
cv2.rectangle(image, (100, 100), (250, 250), (255, 255, 255), -1)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find contours
contours, _ = cv2.findContours(
    gray,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

# Create DifferenceRegion object
region = DifferenceRegion(contours[0])

print("Bounding Box:", region.bounding_box)
print("Center:", region.center)
print("Area:", region.area)

# Draw region
output = region.draw(image.copy())

# Crop region
crop = region.crop_from(image)

# Show results
cv2.imshow("Detected Region", output)
cv2.imshow("Cropped Region", crop)

cv2.waitKey(0)
cv2.destroyAllWindows()
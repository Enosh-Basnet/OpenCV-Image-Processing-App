import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import numpy as np

from processing.image_processor import ImageProcessor


image_a = np.zeros((500, 500, 3), dtype=np.uint8)
image_b = image_a.copy()

# Object added
cv2.rectangle(image_b, (50, 50), (150, 150), (255, 255, 255), -1)

# Object removed
cv2.circle(image_a, (300, 100), 50, (255, 255, 255), -1)

# Colour shift
cv2.rectangle(image_a, (150, 300), (300, 420), (255, 0, 0), -1)
cv2.rectangle(image_b, (150, 300), (300, 420), (0, 0, 255), -1)

processor = ImageProcessor(threshold=30, min_area=100)

alterations = processor.process(image_a, image_b)

print("Alteration count:", len(alterations))

for alteration in alterations:
    print(alteration.to_dict())

annotated_a, annotated_b = processor.create_annotated_images(
    image_a,
    image_b,
    alterations
)

cv2.imshow("Annotated Image A", annotated_a)
cv2.imshow("Annotated Image B", annotated_b)

cv2.waitKey(0)
cv2.destroyAllWindows()
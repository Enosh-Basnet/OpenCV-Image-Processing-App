import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import cv2
import numpy as np

from processing.difference_detector import DifferenceDetector


image_a = np.zeros((400, 400, 3), dtype=np.uint8)
image_b = image_a.copy()

cv2.rectangle(image_b, (100, 100), (250, 250), (255, 255, 255), -1)

detector = DifferenceDetector(threshold=30, min_area=100)

regions = detector.detect(image_a, image_b)

print("Number of regions:", len(regions))

for region in regions:
    print(region.to_dict())
    region.draw(image_b)

cv2.imshow("Image A", image_a)
cv2.imshow("Image B with Detected Difference", image_b)

cv2.waitKey(0)
cv2.destroyAllWindows()
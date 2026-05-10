import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import numpy as np

from processing.image_comparer import ImageComparer


image_a = np.zeros((400, 400, 3), dtype=np.uint8)
image_b = image_a.copy()

cv2.rectangle(image_b, (100, 100), (250, 250), (255, 255, 255), -1)
cv2.circle(image_b, (300, 300), 40, (255, 255, 255), -1)

comparer = ImageComparer(threshold=30, min_area=100)

result = comparer.compare(image_a, image_b)

print("Difference count:", result["difference_count"])

for region in result["regions"]:
    print(region.to_dict())

cv2.imshow("Annotated Image A", result["annotated_image_a"])
cv2.imshow("Annotated Image B", result["annotated_image_b"])

cv2.waitKey(0)
cv2.destroyAllWindows()
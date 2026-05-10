import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
import numpy as np

from models.difference_region import DifferenceRegion
from alterations.colour_shift import ColourShift
from alterations.object_added import ObjectAdded
from alterations.object_removed import ObjectRemoved


image = np.zeros((400, 400, 3), dtype=np.uint8)

cv2.rectangle(image, (100, 100), (250, 250), (255, 255, 255), -1)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

contours, _ = cv2.findContours(
    gray,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

region = DifferenceRegion(contours[0])

colour_shift = ColourShift(region)
object_added = ObjectAdded(region)
object_removed = ObjectRemoved(region)

print(colour_shift.to_dict())
print(object_added.to_dict())
print(object_removed.to_dict())

print("Point inside:", colour_shift.contains_point(150, 150))
print("Point outside:", colour_shift.contains_point(300, 300))

colour_shift.mark_found()
print("After found:", colour_shift.to_dict())
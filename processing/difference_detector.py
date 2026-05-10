import cv2
import numpy as np

from models.difference_region import DifferenceRegion


class DifferenceDetector:
    def __init__(self, threshold=30, min_area=100):
        self.threshold = threshold
        self.min_area = min_area

    def detect(self, image_a, image_b):
        if image_a is None or image_b is None:
            raise ValueError("Both images must be valid.")

        if image_a.shape != image_b.shape:
            raise ValueError("Images must have the same dimensions.")

        gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

        difference = cv2.absdiff(gray_a, gray_b)

        _, threshold_image = cv2.threshold(
            difference,
            self.threshold,
            255,
            cv2.THRESH_BINARY
        )

        contours, _ = cv2.findContours(
            threshold_image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        regions = []

        for contour in contours:
            region = DifferenceRegion(contour)

            if region.is_valid(self.min_area):
                regions.append(region)

        return regions
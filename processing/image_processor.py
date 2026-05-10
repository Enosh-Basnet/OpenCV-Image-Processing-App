import cv2
import numpy as np

from processing.difference_detector import DifferenceDetector
from alterations.colour_shift import ColourShift
from alterations.object_added import ObjectAdded
from alterations.object_removed import ObjectRemoved


class ImageProcessor:
    def __init__(self, threshold=30, min_area=100):
        self.detector = DifferenceDetector(
            threshold=threshold,
            min_area=min_area
        )

    def process(self, image_a, image_b):
        self._validate_images(image_a, image_b)

        regions = self.detector.detect(image_a, image_b)

        alterations = []

        for region in regions:
            alteration = self._classify_region(image_a, image_b, region)
            alterations.append(alteration)

        return alterations

    def process_from_paths(self, image_a_path, image_b_path):
        image_a = cv2.imread(image_a_path)
        image_b = cv2.imread(image_b_path)

        if image_a is None:
            raise ValueError(f"Could not load image A: {image_a_path}")

        if image_b is None:
            raise ValueError(f"Could not load image B: {image_b_path}")

        return self.process(image_a, image_b)

    def create_annotated_images(self, image_a, image_b, alterations):
        annotated_a = image_a.copy()
        annotated_b = image_b.copy()

        for alteration in alterations:
            alteration.region.draw(annotated_a)
            alteration.region.draw(annotated_b)

        return annotated_a, annotated_b

    def _classify_region(self, image_a, image_b, region):
        crop_a = region.crop_from(image_a)
        crop_b = region.crop_from(image_b)

        brightness_a = self._mean_brightness(crop_a)
        brightness_b = self._mean_brightness(crop_b)

        colour_difference = self._mean_colour_difference(crop_a, crop_b)

        if brightness_a < 10 and brightness_b > 10:
            return ObjectAdded(region)

        if brightness_a > 10 and brightness_b < 10:
            return ObjectRemoved(region)

        if colour_difference > 20:
            return ColourShift(region)

        return ColourShift(region)

    def _mean_brightness(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return np.mean(gray)

    def _mean_colour_difference(self, image_a, image_b):
        difference = cv2.absdiff(image_a, image_b)
        return np.mean(difference)

    def _validate_images(self, image_a, image_b):
        if image_a is None or image_b is None:
            raise ValueError("Both images must be valid.")

        if image_a.shape != image_b.shape:
            raise ValueError("Images must have the same dimensions.")

        if len(image_a.shape) != 3 or len(image_b.shape) != 3:
            raise ValueError("Images must be colour images.")
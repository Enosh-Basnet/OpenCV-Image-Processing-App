import cv2

from processing.difference_detector import DifferenceDetector


class ImageComparer:
    def __init__(self, threshold=30, min_area=100):
        self.detector = DifferenceDetector(
            threshold=threshold,
            min_area=min_area
        )

    def compare(self, image_a, image_b):
        regions = self.detector.detect(image_a, image_b)

        annotated_a = image_a.copy()
        annotated_b = image_b.copy()

        for region in regions:
            region.draw(annotated_a)
            region.draw(annotated_b)

        return {
            "regions": regions,
            "annotated_image_a": annotated_a,
            "annotated_image_b": annotated_b,
            "difference_count": len(regions)
        }

    def compare_from_paths(self, image_a_path, image_b_path):
        image_a = cv2.imread(image_a_path)
        image_b = cv2.imread(image_b_path)

        if image_a is None:
            raise ValueError(f"Could not load image A: {image_a_path}")

        if image_b is None:
            raise ValueError(f"Could not load image B: {image_b_path}")

        return self.compare(image_a, image_b)
from dataclasses import dataclass
import cv2
import numpy as np


@dataclass
class DifferenceRegion:
    contour: np.ndarray

    def __post_init__(self):
        self.x, self.y, self.w, self.h = cv2.boundingRect(self.contour)
        self.area = cv2.contourArea(self.contour)

    @property
    def bounding_box(self):
        return self.x, self.y, self.w, self.h

    @property
    def center(self):
        return self.x + self.w // 2, self.y + self.h // 2

    def is_valid(self, min_area=100):
        return self.area >= min_area

    def draw(self, image, color=(0, 0, 255), thickness=2):
        cv2.rectangle(
            image,
            (self.x, self.y),
            (self.x + self.w, self.y + self.h),
            color,
            thickness
        )
        return image

    def crop_from(self, image):
        return image[self.y:self.y + self.h, self.x:self.x + self.w]

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.w,
            "height": self.h,
            "area": self.area,
            "center": self.center
        }
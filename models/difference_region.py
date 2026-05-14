# Import dataclass to create a simple class for storing region data
from dataclasses import dataclass

# Import OpenCV for image processing tasks such as bounding boxes and drawing
import cv2

# Import NumPy because the contour is stored as a NumPy array
import numpy as np


# dataclass automatically creates the basic constructor for this class
@dataclass
class DifferenceRegion:
    # Store the contour of a detected difference region
    contour: np.ndarray

    # This method runs automatically after the dataclass object is created
    def __post_init__(self):
        # Get the x, y position and width, height of the contour's bounding rectangle
        self.x, self.y, self.w, self.h = cv2.boundingRect(self.contour)

        # Calculate the area of the contour
        self.area = cv2.contourArea(self.contour)

    # Return the bounding box values of the region
    @property
    def bounding_box(self):
        return self.x, self.y, self.w, self.h

    # Return the centre point of the region
    @property
    def center(self):
        return self.x + self.w // 2, self.y + self.h // 2

    # Check whether the region is large enough to be counted as a valid difference
    def is_valid(self, min_area=100):
        return self.area >= min_area

    # Draw a rectangle around the difference region on the image
    def draw(self, image, color=(0, 0, 255), thickness=2):
        cv2.rectangle(
            image,
            (self.x, self.y),
            (self.x + self.w, self.y + self.h),
            color,
            thickness
        )
        return image

    # Crop and return only this region from the image
    def crop_from(self, image):
        return image[self.y:self.y + self.h, self.x:self.x + self.w]

    # Convert the region information into a dictionary format
    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.w,
            "height": self.h,
            "area": self.area,
            "center": self.center
        }

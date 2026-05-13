class Alteration:
    def __init__(self, region, name):
        self.region = region
        self.name = name
        self.found = False
#mark
    def mark_found(self):
        self.found = True

    def contains_point(self, x, y):
        rx, ry, rw, rh = self.region.bounding_box

        return (
            rx <= x <= rx + rw and
            ry <= y <= ry + rh
        )

    def to_dict(self):
        return {
            "name": self.name,
            "found": self.found,
            "region": self.region.to_dict()
        }
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Difference:
    x: int
    y: int
    radius: int
    found: bool = False

    @property
    def center(self) -> Tuple[int, int]:
        return self.x, self.y

    def contains(self, px: int, py: int, tolerance: int = 0) -> bool:
        dx = px - self.x
        dy = py - self.y
        r = self.radius + tolerance
        return (dx * dx + dy * dy) <= (r * r)

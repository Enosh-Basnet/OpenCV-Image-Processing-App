import cv2
#file
from processing.difference_generator import DifferenceGenerator


class GameManager:
    def __init__(self, points_per_difference=10, max_mistakes=3):
        self.generator = DifferenceGenerator(difference_count=5)

        self.image_a = None
        self.image_b = None

        self.alterations = []

        self.current_score = 0
        self.total_score = 0
        self.points_per_difference = points_per_difference

        self.mistakes = 0
        self.max_mistakes = max_mistakes

        self.game_started = False
        self.game_complete = False
        self.guesses_locked = False
        self.revealed = False

    def start_new_game(self, image_path):
        self.image_a = cv2.imread(image_path)

        if self.image_a is None:
            raise ValueError(f"Could not load image: {image_path}")

        self.image_b, self.alterations = self.generator.generate(self.image_a)

        self.current_score = 0
        self.mistakes = 0

        self.game_started = True
        self.game_complete = False
        self.guesses_locked = False
        self.revealed = False

    def process_click(self, x, y):
        if not self.game_started:
            raise RuntimeError("Game has not started.")

        if self.guesses_locked:
            return {
                "hit": False,
                "message": "No further guesses are allowed.",
                "current_score": self.current_score,
                "total_score": self.total_score,
                "mistakes": self.mistakes,
                "game_complete": self.game_complete,
                "guesses_locked": self.guesses_locked
            }

        for alteration in self.alterations:
            if not alteration.found and alteration.contains_point(x, y):
                alteration.mark_found()

                self.current_score += self.points_per_difference
                self.total_score += self.points_per_difference

                if self._all_alterations_found():
                    self.game_complete = True
                    self.guesses_locked = True

                return {
                    "hit": True,
                    "message": f"Found: {alteration.name}",
                    "alteration": alteration,
                    "current_score": self.current_score,
                    "total_score": self.total_score,
                    "mistakes": self.mistakes,
                    "remaining": self.get_remaining_count(),
                    "game_complete": self.game_complete,
                    "guesses_locked": self.guesses_locked
                }

        self.mistakes += 1

        if self.mistakes >= self.max_mistakes:
            self.guesses_locked = True

            return {
                "hit": False,
                "message": (
                    f"Too many mistakes. You found "
                    f"{self.get_found_count()} out of {self.get_total_alterations()} differences."
                ),
                "current_score": self.current_score,
                "total_score": self.total_score,
                "mistakes": self.mistakes,
                "remaining": self.get_remaining_count(),
                "game_complete": self.game_complete,
                "guesses_locked": self.guesses_locked
            }

        return {
            "hit": False,
            "message": "No difference found.",
            "current_score": self.current_score,
            "total_score": self.total_score,
            "mistakes": self.mistakes,
            "remaining": self.get_remaining_count(),
            "game_complete": self.game_complete,
            "guesses_locked": self.guesses_locked
        }

    def reveal_unfound(self):
        if not self.game_started:
            raise RuntimeError("Game has not started.")

        for alteration in self.alterations:
            alteration.reveal()

        self.revealed = True
        self.guesses_locked = True

        return {
            "message": "All unfound differences revealed.",
            "current_score": self.current_score,
            "total_score": self.total_score,
            "mistakes": self.mistakes,
            "remaining": self.get_remaining_count(),
            "game_complete": self.game_complete,
            "guesses_locked": self.guesses_locked,
            "revealed": self.revealed
        }

    def get_current_score(self):
        return self.current_score

    def get_total_score(self):
        return self.total_score

    def get_mistakes(self):
        return self.mistakes

    def get_total_alterations(self):
        return len(self.alterations)

    def get_found_count(self):
        return sum(1 for alteration in self.alterations if alteration.found)

    def get_remaining_count(self):
        return self.get_total_alterations() - self.get_found_count()

    def is_game_complete(self):
        return self.game_complete

    def are_guesses_locked(self):
        return self.guesses_locked

    def get_game_state(self):
        return {
            "current_score": self.current_score,
            "total_score": self.total_score,
            "mistakes": self.mistakes,
            "max_mistakes": self.max_mistakes,
            "total_alterations": self.get_total_alterations(),
            "found": self.get_found_count(),
            "remaining": self.get_remaining_count(),
            "game_started": self.game_started,
            "game_complete": self.game_complete,
            "guesses_locked": self.guesses_locked,
            "revealed": self.revealed
        }

    def get_images(self):
        return self.image_a, self.image_b

    def get_display_images(self):
        if self.image_a is None or self.image_b is None:
            return None, None

        display_a = self.image_a.copy()
        display_b = self.image_b.copy()

        for alteration in self.alterations:
            if alteration.found:
                self._draw_circle_around_region(display_a, alteration, (0, 0, 255))
                self._draw_circle_around_region(display_b, alteration, (0, 0, 255))

            elif alteration.revealed:
                self._draw_circle_around_region(display_a, alteration, (255, 0, 0))
                self._draw_circle_around_region(display_b, alteration, (255, 0, 0))

        return display_a, display_b

    def reset_game(self):
        self.image_a = None
        self.image_b = None
        self.alterations = []

        self.current_score = 0
        self.mistakes = 0

        self.game_started = False
        self.game_complete = False
        self.guesses_locked = False
        self.revealed = False

    def _all_alterations_found(self):
        return len(self.alterations) > 0 and all(
            alteration.found for alteration in self.alterations
        )

    def _draw_circle_around_region(self, image, alteration, color):
        x, y, w, h = alteration.region.bounding_box

        center_x = x + w // 2
        center_y = y + h // 2

        radius = max(w, h) // 2 + 15

        cv2.circle(
            image,
            (center_x, center_y),
            radius,
            color,
            3
        )
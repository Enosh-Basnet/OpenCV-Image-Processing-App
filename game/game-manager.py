# Main module for managing the game logic
import cv2

# Importing the DifferenceGenerator class to create image differences
from processing.difference_generator import DifferenceGenerator


# Creating GameManager class
# This class controls the whole game state, scoring, mistakes, and display images
class GameManager:
    def __init__(self, points_per_difference=10, max_mistakes=3):
        # Create a DifferenceGenerator object with 5 differences
        self.generator = DifferenceGenerator(difference_count=5)

        # Store the original image and modified image
        self.image_a = None
        self.image_b = None

        # Store all generated alterations/differences
        self.alterations = []

        # Store current round score and total score
        self.current_score = 0
        self.total_score = 0
        self.points_per_difference = points_per_difference

        # Store mistake count and maximum allowed mistakes
        self.mistakes = 0
        self.max_mistakes = max_mistakes

        # Game status flags
        self.game_started = False
        self.game_complete = False
        self.guesses_locked = False
        self.revealed = False

    # Start a new game using the selected image path
    def start_new_game(self, image_path):
        # Read the selected image using OpenCV
        self.image_a = cv2.imread(image_path)

        # Check if the image was loaded correctly
        if self.image_a is None:
            raise ValueError(f"Could not load image: {image_path}")

        # Generate the modified image and store all difference areas
        self.image_b, self.alterations = self.generator.generate(self.image_a)

        # Reset score and mistakes for the new game
        self.current_score = 0
        self.mistakes = 0

        # Reset game status for a fresh round
        self.game_started = True
        self.game_complete = False
        self.guesses_locked = False
        self.revealed = False

    # Process the player's click position
    def process_click(self, x, y):
        # Check whether the game has started
        if not self.game_started:
            raise RuntimeError("Game has not started.")

        # If guesses are locked, do not allow more clicks
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

        # Loop through all alterations to check if the click is inside a difference region
        for alteration in self.alterations:
            # If the alteration is not already found and the click is inside it
            if not alteration.found and alteration.contains_point(x, y):
                # Mark the alteration as found
                alteration.mark_found()

                # Increase current score and total score
                self.current_score += self.points_per_difference
                self.total_score += self.points_per_difference

                # Check if all differences have been found
                if self._all_alterations_found():
                    self.game_complete = True
                    self.guesses_locked = True

                # Return result for a correct click
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

        # If no alteration was found, increase mistake count
        self.mistakes += 1

        # If maximum mistakes are reached, lock further guesses
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

        # Return result when click is wrong but game is still active
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

    # Reveal all unfound differences
    def reveal_unfound(self):
        # Check whether the game has started
        if not self.game_started:
            raise RuntimeError("Game has not started.")

        # Reveal each alteration
        for alteration in self.alterations:
            alteration.reveal()

        # Set reveal and lock status
        self.revealed = True
        self.guesses_locked = True

        # Return updated game status
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

    # Return current round score
    def get_current_score(self):
        return self.current_score

    # Return total score across games
    def get_total_score(self):
        return self.total_score

    # Return number of mistakes
    def get_mistakes(self):
        return self.mistakes

    # Return total number of alterations/differences
    def get_total_alterations(self):
        return len(self.alterations)

    # Return number of found differences
    def get_found_count(self):
        return sum(1 for alteration in self.alterations if alteration.found)

    # Return number of remaining differences
    def get_remaining_count(self):
        return self.get_total_alterations() - self.get_found_count()

    # Return whether the game is complete
    def is_game_complete(self):
        return self.game_complete

    # Return whether guesses are locked
    def are_guesses_locked(self):
        return self.guesses_locked

    # Return all important game state information as a dictionary
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

    # Return original and modified images
    def get_images(self):
        return self.image_a, self.image_b

    # Return display images with circles drawn around found or revealed differences
    def get_display_images(self):
        # If images are not loaded, return None
        if self.image_a is None or self.image_b is None:
            return None, None

        # Make copies so original stored images are not permanently changed
        display_a = self.image_a.copy()
        display_b = self.image_b.copy()

        # Draw circles for found and revealed differences
        for alteration in self.alterations:
            # Red circle for found differences
            if alteration.found:
                self._draw_circle_around_region(display_a, alteration, (0, 0, 255))
                self._draw_circle_around_region(display_b, alteration, (0, 0, 255))

            # Blue circle for revealed differences
            elif alteration.revealed:
                self._draw_circle_around_region(display_a, alteration, (255, 0, 0))
                self._draw_circle_around_region(display_b, alteration, (255, 0, 0))

        return display_a, display_b

    # Reset the whole game state
    def reset_game(self):
        # Clear images and alterations
        self.image_a = None
        self.image_b = None
        self.alterations = []

        # Reset score and mistakes
        self.current_score = 0
        self.mistakes = 0

        # Reset game status flags
        self.game_started = False
        self.game_complete = False
        self.guesses_locked = False
        self.revealed = False

    # Check if all alterations have been found
    def _all_alterations_found(self):
        return len(self.alterations) > 0 and all(
            alteration.found for alteration in self.alterations
        )

    # Draw a circle around a difference region
    def _draw_circle_around_region(self, image, alteration, color):
        # Get the bounding box of the alteration region
        x, y, w, h = alteration.region.bounding_box

        # Calculate the centre point of the region
        center_x = x + w // 2
        center_y = y + h // 2

        # Calculate circle radius based on region size
        radius = max(w, h) // 2 + 15

        # Draw circle using OpenCV
        cv2.circle(
            image,
            (center_x, center_y),
            radius,
            color,
            3
        )

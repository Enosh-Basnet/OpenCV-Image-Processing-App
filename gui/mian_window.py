import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk

from game.game_manager import GameManager


class MainWindow:
    # Canvas size used to display both images
    DISPLAY_WIDTH = 420
    DISPLAY_HEIGHT = 300

    def __init__(self, root):
        self.root = root
        self.root.title("Spot the Difference")
        self.root.geometry("1050x700")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#f1f5f9")

        # Object that handles the main game logic
        self.game_manager = GameManager()

        # References for images displayed in Tkinter
        self.tk_image_a = None
        self.tk_image_b = None

        # Scale values are used to convert displayed coordinates to original image coordinates
        self.scale_a = 1.0
        self.scale_b = 1.0

        # Offset values help keep images centred and click detection accurate
        self.offset_a_x = 0
        self.offset_a_y = 0
        self.offset_b_x = 0
        self.offset_b_y = 0

        self._build_layout()

    def _build_layout(self):
        # Main background container
        self.main_frame = tk.Frame(self.root, bg="#f1f5f9")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=18)

        # Title section
        self.title_label = tk.Label(
            self.main_frame,
            text="🕵️ Spot the Difference",
            font=("Segoe UI", 24, "bold"),
            bg="#f1f5f9",
            fg="#0f172a"
        )
        self.title_label.pack(pady=(0, 5))

        self.subtitle_label = tk.Label(
            self.main_frame,
            text="Find all hidden differences before making 3 mistakes.",
            font=("Segoe UI", 11),
            bg="#f1f5f9",
            fg="#475569"
        )
        self.subtitle_label.pack(pady=(0, 15))

        # Score information section
        self.info_frame = tk.Frame(self.main_frame, bg="#f1f5f9")
        self.info_frame.pack(pady=(0, 12))

        self.score_label = self._create_info_card(
            self.info_frame,
            "Score",
            "0",
            "#2563eb"
        )

        self.mistakes_label = self._create_info_card(
            self.info_frame,
            "Mistakes",
            "0 / 3",
            "#dc2626"
        )

        self.remaining_label = self._create_info_card(
            self.info_frame,
            "Remaining",
            "0",
            "#16a34a"
        )

        # Game control buttons
        self.button_frame = tk.Frame(self.main_frame, bg="#f1f5f9")
        self.button_frame.pack(pady=(0, 14))

        self.new_game_button = self._create_button(
            self.button_frame,
            "🎮 New Game",
            "#2563eb",
            "#1d4ed8",
            self.start_new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=8)

        self.reveal_button = self._create_button(
            self.button_frame,
            "👁 Reveal",
            "#475569",
            "#334155",
            self.reveal_differences
        )
        self.reveal_button.pack(side=tk.LEFT, padx=8)

        self.reset_button = self._create_button(
            self.button_frame,
            "↻ Reset",
            "#dc2626",
            "#b91c1c",
            self.reset_game
        )
        self.reset_button.pack(side=tk.LEFT, padx=8)

        # Image display section
        self.image_frame = tk.Frame(self.main_frame, bg="#f1f5f9")
        self.image_frame.pack(padx=10, pady=3)

        self.left_panel = self._create_image_panel(self.image_frame, "Original Image")
        self.left_panel.pack(side=tk.LEFT, padx=12)

        self.right_panel = self._create_image_panel(self.image_frame, "Modified Image")
        self.right_panel.pack(side=tk.LEFT, padx=12)

        self.canvas_a = self.left_panel.canvas
        self.canvas_b = self.right_panel.canvas

        # Bind mouse clicks to both images
        self.canvas_a.bind("<Button-1>", self.on_image_click)
        self.canvas_b.bind("<Button-1>", self.on_image_click)

        # Message area for game feedback
        self.message_label = tk.Label(
            self.main_frame,
            text="Load one image to start.",
            font=("Segoe UI", 11, "bold"),
            bg="#dbeafe",
            fg="#1e40af",
            padx=18,
            pady=9
        )
        self.message_label.pack(fill=tk.X, pady=(12, 6))

    def _create_info_card(self, parent, title, value, color):
        # Create a small card used for score, mistakes, and remaining values
        card = tk.Frame(
            parent,
            bg="white",
            width=150,
            height=72,
            highlightbackground="#cbd5e1",
            highlightthickness=1
        )
        card.pack(side=tk.LEFT, padx=8)
        card.pack_propagate(False)

        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9),
            bg="white",
            fg="#64748b"
        )
        title_label.pack(pady=(8, 0))

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 17, "bold"),
            bg="white",
            fg=color
        )
        value_label.pack(pady=(0, 8))

        return value_label

    def _create_image_panel(self, parent, title):
        # Create an image panel with a label and canvas
        panel = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#cbd5e1",
            highlightthickness=1
        )

        label = tk.Label(
            panel,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#0f172a"
        )
        label.pack(pady=(10, 6))

        canvas = tk.Canvas(
            panel,
            width=self.DISPLAY_WIDTH,
            height=self.DISPLAY_HEIGHT,
            bg="#94a3b8",
            highlightthickness=0
        )
        canvas.pack(padx=12, pady=(0, 12))

        panel.canvas = canvas
        return panel

    def _create_button(self, parent, text, bg_color, hover_color, command):
        # Create a styled button with hover effect
        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=bg_color,
            fg="white",
            activebackground=hover_color,
            activeforeground="white",
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2",
            command=command
        )

        button.bind("<Enter>", lambda event: button.config(bg=hover_color))
        button.bind("<Leave>", lambda event: button.config(bg=bg_color))

        return button

    def _set_message(self, text, message_type="info"):
        # Update the message label colour based on message type
        colors = {
            "info": ("#dbeafe", "#1e40af"),
            "success": ("#dcfce7", "#166534"),
            "warning": ("#fef3c7", "#92400e"),
            "error": ("#fee2e2", "#991b1b")
        }

        bg_color, fg_color = colors.get(message_type, colors["info"])

        self.message_label.config(
            text=text,
            bg=bg_color,
            fg=fg_color
        )

    def start_new_game(self):
        # Select an image and start a new game
        image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp"),
                ("All Files", "*.*")
            ]
        )

        if not image_path:
            return

        try:
            self.game_manager.start_new_game(image_path)
            self.refresh_display()
            self._set_message("Game started. Find the 5 differences.", "success")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def on_image_click(self, event):
        # Handle user clicks on either image canvas
        if not self.game_manager.game_started:
            self._set_message("Start a new game first.", "error")
            return

        clicked_canvas = event.widget

        # Convert canvas click position into original image position
        if clicked_canvas == self.canvas_a:
            if self.tk_image_a is None:
                return

            clicked_x = event.x - self.offset_a_x
            clicked_y = event.y - self.offset_a_y

            image_width = self.tk_image_a.width()
            image_height = self.tk_image_a.height()

            if clicked_x < 0 or clicked_y < 0 or clicked_x > image_width or clicked_y > image_height:
                self._set_message("Click inside the image area.", "warning")
                return

            original_x = int(clicked_x / self.scale_a)
            original_y = int(clicked_y / self.scale_a)

        else:
            if self.tk_image_b is None:
                return

            clicked_x = event.x - self.offset_b_x
            clicked_y = event.y - self.offset_b_y

            image_width = self.tk_image_b.width()
            image_height = self.tk_image_b.height()

            if clicked_x < 0 or clicked_y < 0 or clicked_x > image_width or clicked_y > image_height:
                self._set_message("Click inside the image area.", "warning")
                return

            original_x = int(clicked_x / self.scale_b)
            original_y = int(clicked_y / self.scale_b)

        try:
            result = self.game_manager.process_click(original_x, original_y)
            self.refresh_display()

            if result.get("game_complete"):
                self._set_message(result["message"], "success")
                messagebox.showinfo("Game Complete", "You found all differences.")

            elif result.get("guesses_locked"):
                self._set_message(result["message"], "error")
                messagebox.showinfo("Game Over", result["message"])

            else:
                message_text = result["message"]

                if "mistake" in message_text.lower() or "wrong" in message_text.lower():
                    self._set_message(message_text, "error")
                elif "correct" in message_text.lower() or "found" in message_text.lower():
                    self._set_message(message_text, "success")
                else:
                    self._set_message(message_text, "info")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def reveal_differences(self):
        # Reveal all remaining differences
        if not self.game_manager.game_started:
            self._set_message("Start a new game first.", "error")
            return

        try:
            result = self.game_manager.reveal_unfound()
            self._set_message(result["message"], "warning")
            self.refresh_display()

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def reset_game(self):
        # Reset the game and clear the interface
        self.game_manager.reset_game()

        self.canvas_a.delete("all")
        self.canvas_b.delete("all")

        self.tk_image_a = None
        self.tk_image_b = None

        self.scale_a = 1.0
        self.scale_b = 1.0

        self.offset_a_x = 0
        self.offset_a_y = 0
        self.offset_b_x = 0
        self.offset_b_y = 0

        self.score_label.config(text="0")
        self.mistakes_label.config(text="0 / 3")
        self.remaining_label.config(text="0")

        self._set_message("Game reset. Load one image to start.", "info")

    def refresh_display(self):
        # Refresh both images on the screen
        image_a, image_b = self.game_manager.get_display_images()

        if image_a is None or image_b is None:
            return

        self.tk_image_a, self.scale_a = self._convert_cv_image_to_tk(image_a)
        self.tk_image_b, self.scale_b = self._convert_cv_image_to_tk(image_b)

        self.canvas_a.delete("all")
        self.canvas_b.delete("all")

        # Get resized image dimensions
        image_a_width = self.tk_image_a.width()
        image_a_height = self.tk_image_a.height()

        image_b_width = self.tk_image_b.width()
        image_b_height = self.tk_image_b.height()

        # Calculate offsets to centre images inside the canvas
        self.offset_a_x = (self.DISPLAY_WIDTH - image_a_width) // 2
        self.offset_a_y = (self.DISPLAY_HEIGHT - image_a_height) // 2

        self.offset_b_x = (self.DISPLAY_WIDTH - image_b_width) // 2
        self.offset_b_y = (self.DISPLAY_HEIGHT - image_b_height) // 2

        # Draw centred images
        self.canvas_a.create_image(
            self.offset_a_x,
            self.offset_a_y,
            anchor=tk.NW,
            image=self.tk_image_a
        )

        self.canvas_b.create_image(
            self.offset_b_x,
            self.offset_b_y,
            anchor=tk.NW,
            image=self.tk_image_b
        )

        self.update_status_labels()

    def update_status_labels(self):
        # Update score, mistake, and remaining labels
        state = self.game_manager.get_game_state()

        self.score_label.config(text=f"{state['current_score']}")
        self.mistakes_label.config(
            text=f"{state['mistakes']} / {state['max_mistakes']}"
        )
        self.remaining_label.config(text=f"{state['remaining']}")

    def _convert_cv_image_to_tk(self, cv_image):
        # Convert OpenCV image to Tkinter image format
        height, width = cv_image.shape[:2]

        scale = min(
            self.DISPLAY_WIDTH / width,
            self.DISPLAY_HEIGHT / height,
            1.0
        )

        new_width = int(width * scale)
        new_height = int(height * scale)

        resized_image = cv2.resize(
            cv_image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

        # Convert BGR to RGB for correct Tkinter display
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)

        return ImageTk.PhotoImage(pil_image), scale

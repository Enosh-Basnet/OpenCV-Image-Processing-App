# OpenCV Spot the Difference Game

## Overview

This project is an OpenCV-based “Spot the Difference” game developed using Python and Tkinter.

The application allows the user to upload a single image. The system then automatically creates a modified clone containing exactly 5 programmatically generated visual differences. The player must identify all differences by clicking on the images.

The project combines:
- OpenCV image processing
- Tkinter GUI development
- object-oriented programming
- modular software architecture

---

# Features

- Upload a single image
- Automatically generate 5 random differences
- Side-by-side image comparison
- Score tracking system
- Mistake tracking system
- Difference reveal system
- Interactive GUI using Tkinter
- Programmatic image manipulation using OpenCV

---

# Technologies Used

- Python
- OpenCV
- Tkinter
- NumPy
- Pillow (PIL)

---

# Project Architecture

```text
opencv-app/
│
├── alterations/
│   ├── __init__.py
│   ├── alteration.py
│   ├── colour_shift.py
│   ├── object_added.py
│   └── object_removed.py
│
├── assets/
│   └── (images and generated outputs)
│
├── game/
│   ├── __init__.py
│   └── game_manager.py
│
├── gui/
│   ├── __init__.py
│   └── main_window.py
│
├── models/
│   ├── __init__.py
│   ├── alteration.py
│   ├── difference_region.py
│   └── region.py
│
├── processing/
│   ├── __init__.py
│   ├── difference_detector.py
│   ├── difference_generator.py
│   ├── image_comparer.py
│   └── image_processor.py
│
├── tests/
│   ├── __init__.py
│   ├── test_alterations_manual.py
│   ├── test_difference_detector_manual.py
│   ├── test_game_manager_manual.py
│   ├── test_image_comparer_manual.py
│   ├── test_image_processor_manual.py
│   └── test.py
│
├── main.py
├── test_generator.py
└── README.md
```

---

# Architecture Overview

The application follows a modular layered architecture that separates:

- GUI logic
- game management
- image processing
- alteration generation
- data models
- testing

This separation improves:
- maintainability
- scalability
- debugging
- code reuse

---

# Module Responsibilities

## main.py

Application entry point.

Responsibilities:
- starts the Tkinter application
- initializes the main GUI window
- launches the game loop

---

## gui/

Contains all Tkinter GUI components.

### main_window.py

Handles:
- window creation
- image display
- button controls
- user interaction
- click event handling
- UI updates

The GUI layer does not contain gameplay or image-processing logic.

---

## game/

Contains core gameplay management.

### game_manager.py

Acts as the central controller of the application.

Responsibilities:
- manages game state
- tracks score and mistakes
- processes user clicks
- validates found differences
- controls reveal/reset logic
- communicates between GUI and processing modules

---

## processing/

Contains all OpenCV image-processing functionality.

### difference_generator.py

Programmatically creates exactly 5 visual differences in a cloned image.

Current modifications include:
- local colour shifts
- texture replacement
- soft brightness changes
- subtle blur regions
- tiny object insertion

### difference_detector.py

Handles image comparison and difference detection operations.

### image_comparer.py

Provides lower-level image comparison utilities.

### image_processor.py

Coordinates image-processing workflows.

---

## models/

Contains reusable data structures.

### region.py

Represents:
- positional coordinates
- bounding boxes
- click hit detection

### alteration.py

Represents a single game difference.

Stores:
- region information
- found state
- revealed state
- alteration metadata

### difference_region.py

Represents specialized difference-region information used during processing.

---

## alterations/

Contains individual alteration implementations and alteration-specific behaviours.

Examples:
- colour shifting
- object insertion
- object removal

This package allows the generator system to remain modular and extensible.

---

## tests/

Contains manual test modules for validating:
- alteration generation
- image comparison
- difference detection
- game management
- image processing

Used for debugging and validation during development.

---

# Application Workflow

```text
User uploads image
        ↓
GameManager loads image
        ↓
DifferenceGenerator creates modified clone
        ↓
GUI displays original + altered image
        ↓
User clicks suspected differences
        ↓
GameManager validates click regions
        ↓
Score and game state update
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd opencv-app
```

---

## 2. Install Dependencies

```bash
pip install opencv-python pillow numpy
```

---

# Running the Application

```bash
python main.py
```

---

# How to Play

1. Launch the application
2. Click “New Game”
3. Upload an image
4. The application generates 5 hidden differences
5. Find the differences by clicking on the images
6. The game ends when:
   - all differences are found
   - maximum mistakes are reached

---

# Future Improvements

Potential future enhancements include:
- difficulty levels
- timers
- leaderboard system
- semantic object-aware alterations
- animated GUI transitions
- sound effects
- improved image scaling

---


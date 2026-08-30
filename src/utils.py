from pathlib import Path
import pandas as pd

def intro(text: str) -> None:
    """Print a section heading"""
    print("=" * 60)
    print(text)
    print("=" * 60)

def find_root_dir(marker: str = "tfg") -> Path:
    """
    Find a project root directory by its name or marker folder
    """
    current_path = Path.cwd()
    for candidate in [current_path, *current_path.parents]:
        # Case 1: the current candidate is already the root directory.
        if candidate.name == marker:
            return candidate.resolve()
        # Case 2: the root directory is a child of the candidate.
        marker_path = candidate / marker
        if marker_path.is_dir():
            return marker_path.resolve()

    raise FileNotFoundError(f"Could not find '{marker}' folder in {current_path} or its parents")

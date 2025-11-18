"""
Setup script to create the necessary directory structure and move files to their appropriate locations.
"""
import os
import shutil
from pathlib import Path
import sys

def setup_project():
    """
    Setup the project directory structure and move files to their appropriate locations.
    """
    # Get the root directory
    root_dir = Path(__file__).parent
    
    # Create directories if they don't exist
    directories = [
        root_dir / "src",
        root_dir / "src" / "api",
        root_dir / "src" / "ui",
        root_dir / "src" / "utils",
        root_dir / "config",
        root_dir / "assets",
        root_dir / "data",
        root_dir / "storage",
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Move snack.jpg to assets directory if it exists
    snack_image = root_dir / "snack.jpg"
    if snack_image.exists():
        asset_image = root_dir / "assets" / "snack.jpg"
        if not asset_image.exists():
            shutil.copy(snack_image, asset_image)
            print(f"Copied {snack_image} to {asset_image}")
    
    print("Project setup complete!")

if __name__ == "__main__":
    setup_project()
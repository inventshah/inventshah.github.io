"""
Sachin Shah
December 2021

Script to compress images
"""

import os
from PIL import Image

MAX_LENGTH = 300
DIR = "images/"

images = (os.path.join(DIR, file) for file in os.listdir(DIR) if file.endswith(".png"))

for path in images:
    img = Image.open(path)
    width, height = img.size
    if height > MAX_LENGTH or width > MAX_LENGTH:
        factor = MAX_LENGTH / max(height, width)
        img = img.resize((int(width * factor), int(height * factor)))

    img.save(path.replace(".png", ".webp"), format="webp")

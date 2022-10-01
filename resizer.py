"""
Sachin Shah
December 2021

Script to compress images
"""
import os
import cv2

MAX_LENGTH = 300
DIR = "images/"

images = (os.path.join(DIR, file) for file in os.listdir(DIR) if file.endswith(".png"))

for path in images:
    img = cv2.imread(path)
    height, width, channels = img.shape
    if height < MAX_LENGTH > width:
        continue

    factor = MAX_LENGTH / max(height, width)

    img = cv2.resize(
        img, (int(width * factor), int(height * factor)), interpolation=cv2.INTER_AREA
    )

    cv2.imwrite(path, img)

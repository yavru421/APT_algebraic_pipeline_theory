# m2: Image upload module (APT-compliant)
# Input: x1 (file_path) -> Output: y2 (uploaded_path)
# Equation: y2 = m2(x1)

import os

SCORE_FOLDER = "score"

def m2_upload_image(file_path):
    """
    APT Module: m2
    Input: file_path (str) - Source image file path
    Output: uploaded_path (str) - Destination path in score folder
    Equation: y2 = m2(x1)

    Description: Uploads/copies image to score folder for processing
    """
    if not os.path.exists(SCORE_FOLDER):
        os.makedirs(SCORE_FOLDER)
    dest = os.path.join(SCORE_FOLDER, os.path.basename(file_path))

    # If the file is already in the score folder, don't copy it to itself
    if os.path.abspath(file_path) == os.path.abspath(dest):
        print(f"APT m2: File already in score folder, returning as-is: {dest}")
        return dest

    # Copy file to score folder
    with open(file_path, "rb") as src, open(dest, "wb") as dst:
        dst.write(src.read())
    return dest
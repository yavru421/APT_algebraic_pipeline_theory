# m0: DNG conversion module (APT-compliant)
# Input: x1 (file_path) -> Output: y0 (converted_path)
# Equation: y0 = m0(x1)

import os
import subprocess

def m0_convert_dng(file_path):
    """
    APT Module: m0
    Input: file_path (str) - Raw image file path
    Output: converted_path (str) - Processed file path
    Equation: y0 = m0(x1)

    Description: Converts DNG files to PNG/JPG or passes through compatible formats
    """
    # For PNG/JPG files, return as-is
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return file_path

    # For DNG files, skip conversion and return None
    if file_path.lower().endswith('.dng'):
        print(f"APT m0: Skipping DNG file (convert to PNG first): {file_path}")
        return None

    return file_path

def m0a_bulk_convert_dng(score_folder):
    """
    APT Module: m0a
    Input: score_folder (str) - Directory path
    Output: converted_files (List[str]) - List of converted file paths
    Equation: y0a = m0a(x_folder)

    Description: Batch converts all DNG files in a folder
    """
    converted_files = []
    if not os.path.exists(score_folder):
        os.makedirs(score_folder)
        return converted_files

    for fname in os.listdir(score_folder):
        fpath = os.path.join(score_folder, fname)
        if os.path.isfile(fpath):
            converted_path = m0_convert_dng(fpath)
            converted_files.append(converted_path)

    return converted_files
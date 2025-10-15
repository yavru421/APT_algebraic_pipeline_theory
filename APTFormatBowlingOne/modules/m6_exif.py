import os
from PIL import Image, ExifTags


def m6_extract_exif_metadata(file_path):
    """
    Simple EXIF extraction. Returns a short summary string or empty string if not available.
    """
    if not os.path.exists(file_path):
        return ""
    try:
        img = Image.open(file_path)
        exif = img._getexif() or {}
        # Map tag ids to names and build a small summary
        summary_items = []
        for tag_id, value in (exif.items() if isinstance(exif, dict) else []):
            name = ExifTags.TAGS.get(tag_id, tag_id)
            summary_items.append(f"{name}: {value}")
            # limit output
            if len(summary_items) >= 5:
                break
        return " | ".join(summary_items)
    except Exception:
        return ""

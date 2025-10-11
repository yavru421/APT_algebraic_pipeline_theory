# m14: Smart processing module (APT-compliant)
# Input: x3 (score_folder), x4 (records_file) -> Output: y14 (smart_results)
# Equation: y14 = m14(x3, x4)

import os
from .m13_load import m13_load_bowling_records
from .m12_save import m12_save_bowling_records
from .m0_dng_convert import m0_convert_dng
from .m2_upload import m2_upload_image
from .m6_exif import m6_extract_exif_metadata

def m14_smart_process_images(score_folder, records_file="bowling_records.json"):
    """
    APT Module: m14
    Input: score_folder (str), records_file (str)
    Output: smart_results (List[Dict]) - Combined cached and new results
    Equation: y14 = m14(x3, x4)

    Description: Intelligently processes only new images using cache from JSON records
    """
    # Load existing records
    records = m13_load_bowling_records(records_file)
    processed_files = {game['filename'] for game in records['games']}

    # Get all files in score folder
    if not os.path.exists(score_folder):
        print(f"APT m14: Score folder {score_folder} does not exist")
        return []

    files_found = os.listdir(score_folder)
    new_files = [f for f in files_found if f not in processed_files and os.path.isfile(os.path.join(score_folder, f))]

    print(f"APT m14: Found {len(files_found)} total files, {len(new_files)} new files to process")

    # Process only new files
    if new_files:
        print(f"APT m14: Processing new files: {new_files}")
        new_results = []
        for fname in new_files:
            fpath = os.path.join(score_folder, fname)
            try:
                x1a = m0_convert_dng(fpath)
                if x1a is None:
                    continue

                y2 = m2_upload_image(x1a)

                # Skip API call if file is too large or already processed
                import base64
                from PIL import Image
                if not os.path.exists(y2) or os.path.getsize(y2) == 0:
                    continue

                file_size = os.path.getsize(y2)
                if file_size > 5 * 1024 * 1024:  # 5MB
                    try:
                        img = Image.open(y2)
                        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                        temp_path = y2.replace('.png', '_resized.png').replace('.jpg', '_resized.jpg')
                        img.save(temp_path, optimize=True, quality=85)
                        y2 = temp_path
                    except Exception as resize_error:
                        print(f"APT m14: Resize failed for {fname}: {resize_error}")
                        continue

                with open(y2, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')

                # API call
                from llama_api_client import LlamaAPIClient
                try:
                    client = LlamaAPIClient()
                    response = client.chat.completions.create(
                        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                        messages=[{
                            "role": "user",
                            "content": [{
                                "type": "text",
                                "text": f"Extract all bowling scores, player names, dates, or game information from this image. Image filename: {fname}",
                            }, {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{image_data}"}
                            }]
                        }]
                    )
                    y4 = response.completion_message.content.text
                except Exception as api_error:
                    y4 = f"API Error: {api_error}"

                y6 = m6_extract_exif_metadata(y2)

                new_results.append({
                    "filename": fname,
                    "llama_data": y4,
                    "exif": y6
                })

            except Exception as err:
                print(f"APT m14: Error processing {fname}: {err}")
                new_results.append({
                    "filename": fname,
                    "llama_data": f"Error: {err}",
                    "exif": ""
                })

        # Save new results to records
        if new_results:
            updated_records = m12_save_bowling_records(new_results, records_file)

    # Convert all records back to structured format for the leaderboard
    all_results = []
    for game in records['games']:
        # Pass the structured game data directly (includes 'players' array)
        all_results.append(game)

    return all_results
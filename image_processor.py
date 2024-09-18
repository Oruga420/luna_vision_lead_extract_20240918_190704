import csv
import os
import io
from PIL import Image
from openai_handler import extract_info_from_image

def process_images(image_paths):
    results = []
    for image_path in image_paths:
        print(f"Processing image: {image_path}")
        with Image.open(image_path) as img:
            img.thumbnail((1024, 1024))
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            info = extract_info_from_image(img_byte_arr)
            if 'error' in info:
                print(f"Error processing image {image_path}: {info['error']}")
                continue
            results.append(info)
    
    if not results:
        return None

    csv_path = 'extracted_info.csv'
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Email', 'Name', 'Last Name', 'Phone', 'Extra Info']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({field: result.get(field, '') for field in fieldnames})
    
    return csv_path

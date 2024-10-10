import os
from PIL import Image
import numpy as np

def remove_greyscale(input_folder, output_folder):
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]
    threshold = 100
    

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        img = Image.open(image_path)
        img_width, img_height = img.size

        img_greyscale = img.convert('L')
        img_upscaled = img_greyscale.resize(size=(img_width*4, img_height*4), resample = Image.LANCZOS)
        img_arr = np.array(img_upscaled)
        img_arr[img_arr < threshold] = 0
        img_arr[img_arr >= threshold] = 255
        img_final = Image.fromarray(np.uint8(img_arr))

        img_final.save(os.path.join(output_folder, "no_grayscale_" + image_file))

        
input_folder = 'input'
output_folder = 'no_greyscale'
remove_greyscale(input_folder, output_folder)
print("Removed greyscale from images in input folder, check output folder.")
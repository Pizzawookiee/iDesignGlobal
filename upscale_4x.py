import os
from PIL import Image
import numpy as np

def upscale_4x(input_folder, output_folder):
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]
    threshold = 100
    

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        img = Image.open(image_path)
        img_width, img_height = img.size

        img_upscaled = img.resize(size=(img_width*4, img_height*4), resample = Image.LANCZOS)


        img_upscaled.save(os.path.join(output_folder, "upscaled_4x_" + image_file))

        
input_folder = 'input'
output_folder = 'upscaled_4x'
upscale_4x(input_folder, output_folder)
print("Upscaled images 4x from input folder, check output folder.")
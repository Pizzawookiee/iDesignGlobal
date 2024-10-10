#https://huggingface.co/briaai/RMBG-1.4/blob/main/example_inference.py
#https://huggingface.co/briaai/RMBG-1.4/blob/main/utilities.py

from enum import StrEnum, auto
import os
from PIL import Image
import numpy as np
import onnxruntime as ort
class InferenceDevice(StrEnum):
    cpu = auto()
    cuda = auto()

onnx_model = 'model_fp16.onnx'

sess_options = ort.SessionOptions()
sess_options.enable_profiling = False
device = InferenceDevice.cpu
providers = ["CPUExecutionProvider"]
session = ort.InferenceSession(
        onnx_model, sess_options=sess_options, providers=providers
    )




def remove_background(input_folder, output_folder):
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]
    threshold = 100
    

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        img = Image.open(image_path)
        img_size = img.size
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
      

        input = img.resize([1024, 1024], Image.BILINEAR)
        
        input = np.array(input).astype(np.float32)
        if len(input.shape) < 3:
            input = input [:,:,np.newaxis]
        input = np.transpose(input, (2,0,1))/255.0
        
        input = np.expand_dims(input,axis=0)
        #input = (input - input.max())/(input.max()-input.min())
        input = (input - 0.5)/(1)
        
        input = input.astype(np.float32)
        
        
        binding = session.io_binding()
        ort_input = session.get_inputs()[0].name
        binding.bind_cpu_input(ort_input, input)
        ort_output = session.get_outputs()[0].name
        binding.bind_output(ort_output, device.value)

        session.run_with_iobinding(binding)  # Actual inference happens here.

        mask = binding.get_outputs()[0].numpy()
        mask = mask[0][0]
        #print(mask.shape)
        mask = (mask - mask.min())/(mask.max() - mask.min())
        mask = np.transpose(mask * 255, (0,1)).astype(np.uint8)
        #mask = np.squeeze(mask)
        mask = Image.fromarray(mask).resize(img_size, Image.BILINEAR)
        
        no_bg_image = Image.new("RGBA", img_size, (0,0,0,0))
        no_bg_image.paste(img, mask = mask)
        result = no_bg_image
        
        base, extension = image_file.rsplit('.', 1)

        # Check if the extension is not 'png'
        if extension != 'png':
            image_file = base + '.png'


        result.save(os.path.join(output_folder, "remove_background_" + image_file))

        
input_folder = 'input'
output_folder = 'remove_background'
remove_background(input_folder, output_folder)
print("Removed backgrounds from input folder, check output folder.")
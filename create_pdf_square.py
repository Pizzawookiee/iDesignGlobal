import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

square = (8.5 * 72, 8.5 * 72)

def create_pdf_from_images(input_folder, output_file):
    c = canvas.Canvas(output_file, pagesize=square)
    page_width, page_height = square
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]
    black_page = Image.new(mode = "RGB", size=(750, 800)) #letter dimensions minus margins
    b_image = io.BytesIO()
    black_page.save(b_image, format='png')
    b_image.seek(0)
    b_image_data = ImageReader(b_image)

    bw, bh = black_page.size
    ml = 0.25 * 72 #left margin for black page
    mr = 0.75 * 72 #right margin for black page
    mt = 0.25 * 72 #top margin for black page
    mb = 0.25 * 72 #bottom margin for black page
    mw = page_width - ml - mr
    mh = page_height - mt - mb
    s = min(mw/bw,mh/bh) #scaling factor for black page
    bw_scaled = bw * s
    bh_scaled = bh * s
    bx = (page_width - bw_scaled) / 2 - 0.25 * 72
    by = (page_height - bh_scaled) / 2

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        img = Image.open(image_path)
        img_width, img_height = img.size

        # Calculate position and size for the image
        margin_left = 0.75 * 72  # Convert inches to points
        margin_right = 0.25 * 72  # Convert inches to points
        
        max_width = page_width - margin_left - margin_right
        max_height = page_height
        scale = min(max_width / img_width, max_height / img_height)
        image_width = img_width * scale
        image_height = img_height * scale

        # Calculate position for the image
        x = (page_width - image_width) / 2 + 0.25 * 72
        y = (page_height - image_height) / 2

        # Draw image centered on the page, insert image page
        c.drawImage(image_path, x, y, width=image_width, height=image_height)
        c.showPage()

        # Insert black page (deprecated)
        #c.setFillColorRGB(0, 0, 0)  # Set fill color to black
        #c.rect(0, 0, page_width, page_height, fill=1)  # Draw a filled black rectangle covering the entire page
        #c.showPage()

        # Insert black page
        c.drawImage(b_image_data, bx,by,width = bw_scaled, height = bh_scaled)
        c.showPage()

    c.save()

input_folder = 'input'
output_file = 'output_square.pdf'
create_pdf_from_images(input_folder, output_file)
print("PDF created successfully.")
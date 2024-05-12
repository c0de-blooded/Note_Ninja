import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    text = ""
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    # Iterate over each page
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Extract text from text slides
        text += page.get_text()
        
        # Extract text from images using OCR (Optical Character Recognition)
        images = page.get_images(full=True)
        for img_index, img_info in enumerate(images):
            xref = img_info[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            text += pytesseract.image_to_string(image)
    
    pdf_document.close()
    
    return text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

pdf_path = "Therapie.pdf"
output_file = "output_text.txt"

text_from_pdf = extract_text_from_pdf(pdf_path)
save_text_to_file(text_from_pdf, output_file)
print(text_from_pdf)


# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from reportlab.lib.units import inch
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import Paragraph

# def text_to_pdf(input_file, output_file):
#     # Create a canvas
#     c = canvas.Canvas(output_file, pagesize=letter)
#     width, height = letter
    
#     # Open the text file and read its content
#     with open(input_file, 'r') as f:
#         text = f.read()
    
#     # Set font and calculate text size
#     style = getSampleStyleSheet()["Normal"]
#     text_object = Paragraph(text, style=style)
#     text_width, text_height = text_object.wrap(width, height)
    
#     # Calculate the position to center text horizontally and vertically
#     x = (width - text_width) / 2
#     y = (height - text_height) / 2
    
#     # Draw the text on the canvas
#     text_object.drawOn(c, x, y)
    
#     # Save the PDF
#     c.save()

# # Usage example
# text_to_pdf("output_text.txt", "output.pdf")


import textwrap
from fpdf import FPDF

def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)

    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            # Encode text to Latin-1, ignoring any characters that can't be encoded
            wrap_encoded = wrap.encode('latin-1', 'ignore').decode('latin-1')
            pdf.cell(0, fontsize_mm, wrap_encoded, ln=1)

    pdf.output(filename, 'F')

input_filename = 'output_text.txt'
output_filename = 'output.pdf'
with open(input_filename, 'r', encoding='utf-8') as file:
    text = file.read()
text_to_pdf(text, output_filename)
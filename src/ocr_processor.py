# script for OCR processing
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re

def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert('L')
    image = ImageEnhance.Contrast(image).enhance(2)
    image = ImageEnhance.Sharpness(image).enhance(2)
    image = image.filter(ImageFilter.MedianFilter())
    return image

def ocr_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed_image)
    return text 

def parse_text(text):
    items_prices = re.findall(r'(\w+.*?)\s+(\d+)', text)
    return items_prices
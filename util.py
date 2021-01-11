import configparser
import json
import re, pytesseract, requests
from io import BytesIO
from PIL import Image

def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

def get_coin_name(text):
    if len(name := re.findall(r"[\$S]([A-z]{3,5})", text)) > 0:
        return name[0]
    return None

def ocr_image(image):
    print("- Doing OCR -")
    return str(((pytesseract.image_to_string(image)))) 

def get_image(url):
    print(f"Getting: {url}")
    r = requests.get(url)

    assert r.status_code == 200, "image not found"
    return Image.open(BytesIO(r.content))
import configparser
import json
import re, pytesseract

def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

def get_coin_name(text):
    if len(name := re.findall(r"[\$S]([A-Z]{3,4})", text)) > 0:
        return name[0]
    return None

def ocr_image(image):
    print("- Doing OCR -")
    return str(((pytesseract.image_to_string(image)))) 
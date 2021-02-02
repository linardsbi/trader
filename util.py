import configparser
import json
import re, pytesseract, requests
from io import BytesIO
from PIL import Image

def print_for_web_only(price):
    import pyperclip
    print("Make a limit sell at:")
    print("for 10x: %f" % (price * 10))
    print("for  8x: %f" % (price * 8))
    print("for  4x: %f" % (price * 4))
    print("for  2x: %f" % (price * 2))
    pyperclip.copy(format(price * 4, "f"))

def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

def get_coin_name(text):
    if len(name := re.findall(r":*\s*[\$S]([A-z]{3,5})", text)) > 0:
        return str(name[0]).upper()
    return None

def ocr_image(image):
    return str(((pytesseract.image_to_string(image)))) 

def get_image(url):
    print(f"Getting: {url}")
    r = requests.get(url)

    assert r.status_code == 200, "image not found"
    return Image.open(BytesIO(r.content))
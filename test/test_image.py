import unittest
from PIL import Image, ImageDraw, ImageFont
import sys

from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import util

def make_image(text, size=48):
    try:
        fnt = ImageFont.truetype('arial.ttf', size)
    except Exception:
        fnt = ImageFont.truetype('FreeSerif.otf', size)

    image = Image.new(mode = "RGB", size = (int(size)*len(text),size+250), color = "white")

    draw = ImageDraw.Draw(image)
    draw.text((50,50), text, (0,0,0), font=fnt)

    return image

class TestImageRecognition(unittest.TestCase):
    def test_recognise_text_random(self):
        def get_random_string(length) -> str:
            import random, string
            letters = string.ascii_lowercase + ' '
            return ''.join([random.choice(letters) for i in range(length)])

        image = make_image(get_random_string(150))
        text = util.ocr_image(image)
        self.assertTrue(text, "No text recognized")
        name = util.get_coin_name(text)
        self.assertFalse(name, f"Regex error: {name} found in random text")

    def test_recognise_text(self):
        coin = "BTC"
        image = make_image(f"Coin is: ${coin}")
        text = util.ocr_image(image)

        self.assertTrue(text, "No text recognized")

        name = util.get_coin_name(text)

        self.assertIsNotNone(name, "No coin name recognized")
        self.assertTrue(name == coin, f"Regex error: {coin} not found in text")

if __name__ == '__main__':
    unittest.main()

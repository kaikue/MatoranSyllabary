import sys
from PIL import Image, ImageDraw

"""
TODO:
draw vowels
draw consonants
support full words
support aspirated consonants
support codas
"""

BG_COLOR = (224, 224, 224)
LINE_COLOR = (32, 32, 32)
FILL_COLOR = BG_COLOR
SIZE = 128
SPACING = 10
BASE_WIDTH = 10
LETTER_WIDTH = 5
VOWEL_SIZE = SIZE / 4

VOWEL_DIST = 0.5

VOWELS = ["a", "e", "i", "o", "u"]
LETTERS = {
    "a": [{
            "type": "circle",
            "x": 0,
            "y": VOWEL_DIST
        }],
    "e": [{
            "type": "circle",
            "x": VOWEL_DIST,
            "y": 0
        }],
    "i": [{
            "type": "circle",
            "x": 0,
            "y": -VOWEL_DIST
        }],
    "o": [{
            "type": "circle",
            "x": 0,
            "y": 0
        }],
    "u": [{
            "type": "circle",
            "x": -VOWEL_DIST,
            "y": 0
        }]
}

def draw_base(draw, x):
    draw.ellipse((x, SPACING, x + SIZE, SPACING + SIZE), fill=FILL_COLOR, outline=LINE_COLOR, width=BASE_WIDTH)

def draw_letter(letter, draw, x):
    shapes = LETTERS[letter]
    cx = x + SIZE / 2
    cy = SPACING + SIZE / 2
    for shape in shapes:
        if shape["type"] == "circle":
            ccx = cx + shape["x"] * SIZE / 2
            ccy = cy + shape["y"] * SIZE / 2
            circle_x = ccx - VOWEL_SIZE / 2
            circle_y = ccy - VOWEL_SIZE / 2
            draw.ellipse((circle_x, circle_y, circle_x + VOWEL_SIZE, circle_y + VOWEL_SIZE), fill=FILL_COLOR, outline=LINE_COLOR, width=LETTER_WIDTH)
        elif shape["type"] == "line":
            pass #TODO

def main():
    word = sys.argv[1:]
    width = len(word) * (SIZE + SPACING) + SPACING
    height = SIZE + 2 * SPACING
    img = Image.new("RGB", (width, height), BG_COLOR)
    for i in range(len(word)):
        syllable = word[i]
        draw = ImageDraw.Draw(img)
        x = i * (SIZE + SPACING) + SPACING
        draw_base(draw, x)
        for letter in syllable:
            draw_letter(letter, draw, x)
    img.save("_".join(word) + ".png")

if __name__ == "__main__":
    main()
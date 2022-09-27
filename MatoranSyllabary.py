import sys
from turtle import width
from PIL import Image, ImageDraw

"""
TODO:
draw vowels
draw consonants
support full words
support aspirated consonants
support codas
"""

TRANSPARENT = (0, 0, 0, 0)
BG_COLOR = (240, 240, 240)
LINE_COLOR = (16, 16, 16)
FILL_COLOR = BG_COLOR
SIZE = 128
SPACING = 10
BASE_WIDTH = 10
CONSONANT_WIDTH = 8
CONSONANT_WIDTH_ASPIRATED = 10
CONSONANT_GAP_ASPIRATED = 4
VOWEL_WIDTH = 5
VOWEL_SIZE = SIZE / 4

VOWEL_DIST = 0.5
CORNER_DIST = 0.65
FULL_DIST = 0.85
NM_DIST_1 = 0.45
NM_DIST_2 = 0.8

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
        }],
    "h": [{
        "type": "line",
        "x1": -FULL_DIST,
        "y1": 0,
        "x2": FULL_DIST,
        "y2": 0
    }],
    "l": [{
        "type": "line",
        "x1": 0,
        "y1": -FULL_DIST,
        "x2": 0,
        "y2": FULL_DIST
    }],
    "z": [{
        "type": "line",
        "x1": -CORNER_DIST,
        "y1": CORNER_DIST,
        "x2": CORNER_DIST,
        "y2": -CORNER_DIST
    }],
    "s": [{
        "type": "line",
        "x1": -CORNER_DIST,
        "y1": -CORNER_DIST,
        "x2": CORNER_DIST,
        "y2": CORNER_DIST
    }],
    "t": [{
        "type": "line",
        "x1": 0,
        "y1": 0,
        "x2": 0,
        "y2": FULL_DIST
        },
        {
        "type": "line",
        "x1": -FULL_DIST,
        "y1": 0,
        "x2": FULL_DIST,
        "y2": 0
    }],
    "d": [{
        "type": "line",
        "x1": 0,
        "y1": 0,
        "x2": 0,
        "y2": -FULL_DIST
        },
        {
        "type": "line",
        "x1": -FULL_DIST,
        "y1": 0,
        "x2": FULL_DIST,
        "y2": 0
    }],
    "p": [{
        "type": "line",
        "x1": 0,
        "y1": 0,
        "x2": -FULL_DIST,
        "y2": 0
        },
        {
        "type": "line",
        "x1": 0,
        "y1": -FULL_DIST,
        "x2": 0,
        "y2": FULL_DIST
    }],
    "b": [{
        "type": "line",
        "x1": 0,
        "y1": 0,
        "x2": FULL_DIST,
        "y2": 0
        },
        {
        "type": "line",
        "x1": 0,
        "y1": -FULL_DIST,
        "x2": 0,
        "y2": FULL_DIST
    }],
    "k": [{
        "type": "line",
        "x1": -FULL_DIST,
        "y1": 0,
        "x2": FULL_DIST,
        "y2": 0
        },
        {
        "type": "line",
        "x1": 0,
        "y1": -FULL_DIST,
        "x2": 0,
        "y2": FULL_DIST
    }],
    "n": [{
        "type": "line",
        "x1": -NM_DIST_2,
        "y1": -NM_DIST_1,
        "x2": NM_DIST_2,
        "y2": -NM_DIST_1
        },
        {
        "type": "line",
        "x1": -NM_DIST_2,
        "y1": NM_DIST_1,
        "x2": NM_DIST_2,
        "y2": NM_DIST_1
    }],
    "m": [{
        "type": "line",
        "x1": -NM_DIST_1,
        "y1": -NM_DIST_2,
        "x2": -NM_DIST_1,
        "y2": NM_DIST_2
        },
        {
        "type": "line",
        "x1": NM_DIST_1,
        "y1": -NM_DIST_2,
        "x2": NM_DIST_1,
        "y2": NM_DIST_2
    }]
}

def draw_base(draw, x):
    #draw.ellipse((x-1, SPACING-1, x + SIZE+1, SPACING + SIZE+1), fill=FILL_COLOR, outline=(192, 0, 0), width=BASE_WIDTH + 2)
    draw.ellipse((x, SPACING, x + SIZE, SPACING + SIZE), fill=TRANSPARENT, outline=LINE_COLOR, width=BASE_WIDTH)

def draw_letter(letter, draw, x, affix_to, aspirated):
    shapes = LETTERS[letter]
    cx = x + SIZE / 2
    cy = SPACING + SIZE / 2
    aspiration_queue = []
    for shape in shapes:
        if shape["type"] == "circle":
            ccx = cx + shape["x"] * SIZE / 2
            ccy = cy + shape["y"] * SIZE / 2
            circle_x = ccx - VOWEL_SIZE / 2
            circle_y = ccy - VOWEL_SIZE / 2
            draw.ellipse((circle_x, circle_y, circle_x + VOWEL_SIZE, circle_y + VOWEL_SIZE), fill=FILL_COLOR, outline=LINE_COLOR, width=VOWEL_WIDTH)
        elif shape["type"] == "line":
            #TODO if affix_to is not None: position it inside that vowel instead
            x1 = cx + shape["x1"] * SIZE / 2
            y1 = cy + shape["y1"] * SIZE / 2
            x2 = cx + shape["x2"] * SIZE / 2
            y2 = cy + shape["y2"] * SIZE / 2
            if aspirated:
                draw.line((x1, y1, x2, y2), fill=LINE_COLOR, width=CONSONANT_WIDTH_ASPIRATED)
                aspiration_queue.append((x1, y1, x2, y2))
            else:
                draw.line((x1, y1, x2, y2), fill=LINE_COLOR, width=CONSONANT_WIDTH)
    for line in aspiration_queue:
        draw.line(line, fill=BG_COLOR, width=CONSONANT_GAP_ASPIRATED)

def main():
    word = sys.argv[1:]
    width = len(word) * (SIZE + SPACING) + SPACING
    height = SIZE + 2 * SPACING
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img, "RGBA")
    for i in range(len(word)):
        syllable = word[i]
        x = i * (SIZE + SPACING) + SPACING
        last_seen_vowel = None
        j = 0
        while j < len(syllable):
            letter = syllable[j]
            affix_to = None
            if letter in VOWELS:
                last_seen_vowel = letter
            elif last_seen_vowel is not None:
                affix_to = last_seen_vowel
            aspirated = False
            if j + 1 < len(syllable) and syllable[j + 1] == "h":
                aspirated = True
                j += 1
            draw_letter(letter, draw, x, affix_to, aspirated)
            j += 1
        draw_base(draw, x)
    img.save("_".join(word) + ".png")

if __name__ == "__main__":
    main()
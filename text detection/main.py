import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import time


## manual loading


# # read image
# image_path = "C:/Users/asjos/Downloads/boggl/text detection/bog2.png"

# img = cv2.imread(image_path)

## manual loading

time.sleep(1)


## auto capture

import mss.tools

with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": 400, "left": 1000, "width": 550, "height": 550}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    ## save sct_img to file

    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)

    img = cv2.imread(output)


## auto capture


# Preprocessing to enhance contrast
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# You can try different preprocessing techniques such as thresholding or adaptive thresholding
# Example:
# _, img_proc = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Scale up the image for better readability
# img_proc = cv2.resize(gray, interpolation=cv2.INTER_CUBIC)
configs = [
    {
        "contrast_ths": 0.35,
        "adjust_contrast": 0.07,
        "add_margin": 0.15,
        "width_ths": 0.02,
        "batch_size": 5,
        "mag_ratio": 8,
        "min_size": 30,
    },
    {
        "contrast_ths": 0.75,
        "adjust_contrast": 0.87,
        "add_margin": 0.25,
        "width_ths": 0.02,
        "batch_size": 5,
        "mag_ratio": 80,
        "min_size": 30,
    },
]
detected_letters = []

for config in configs:
    # instance text detector
    reader = easyocr.Reader(["en"])

    # detect text on image
    text_ = reader.readtext(
        gray,
        decoder="wordbeamsearch",
        blocklist="0123456789",
        contrast_ths=configs[0]["contrast_ths"],
        adjust_contrast=configs[0]["adjust_contrast"],
        add_margin=configs[0]["add_margin"],
        width_ths=configs[0]["width_ths"],
        batch_size=configs[0]["batch_size"],
        mag_ratio=configs[0]["mag_ratio"],
        min_size=configs[0]["min_size"],
    )

    wrong = ["DIL", "DL", "DLI", "ZX", "TL"]

    threshold = 0.2
    # draw bbox and text
    for t_, t in enumerate(text_):
        print(t)

        bbox, text, score = t

        # if text.upper() not in wrong:
        if len(text) == 1:
            #         if score > threshold:

            detected_letters.append(text.upper())

            start_point = tuple([int(val) for val in bbox[0]])
            end_point = tuple([int(val) for val in bbox[2]])
            cv2.rectangle(img, start_point, end_point, (0, 255, 0), 5)
            cv2.putText(
                img,
                text,
                start_point,
                cv2.FONT_HERSHEY_COMPLEX,
                0.65,
                (255, 0, 0),
                2,
            )

    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.show()

    for i in detected_letters:
        if len(i) != 1:
            detected_letters.remove(i)

    print(detected_letters, len(detected_letters))

    if len(detected_letters) == 25:
        break

    # split detected letters into 5x5 grid into format of "IAAYS,TYWDG,BDDTI,CPANO,MAIDN"

if len(detected_letters) != 25:
    print("Error: Detected letters are not 25")
    exit()


detected_grid = ""

for i in range(0, 25, 5):
    detected_grid += "".join(detected_letters[i : i + 5]) + ","

detected_grid = detected_grid[:-1]
print(detected_grid)


## Boggler

from random import choice
from string import ascii_uppercase
import logging
import time


def timeit(method):
    """Calculates time taken to run a function when called"""

    def timed(*args, **kw):
        t1 = time.time()
        result = method(*args, **kw)
        print(f"{method.__name__!r} {time.time() - t1:.2f} sec")
        return result

    return timed


def get_neighbours():
    """Return a dictionary with all the neighbours surrounding a particular position"""
    neighbours = {}
    # assume grid is a global variable here; define it if not
    for position in grid:
        x, y = position
        positions = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
            (x, y + 1),
            (x - 1, y + 1),
            (x - 1, y),
        ]
        neighbours[position] = [p for p in positions if 0 <= p[0] < X and 0 <= p[1] < Y]
    return neighbours


def path_to_word(path):
    """Convert a list of grid positions to a word"""
    return "".join(grid[p] for p in path)


def search(path):
    """Recursively search the grid for words"""
    word = path_to_word(path)
    logging.debug(f"{path}: {word}")
    if word not in stems:
        return
    if word in dictionary:
        paths.append(path)
    for next_pos in neighbours[path[-1]]:
        if next_pos not in path:
            search(path + [next_pos])


def get_dictionary():
    """Return a list of uppercase english words, including word stems"""
    stems, dictionary = set(), set()
    with open("words.txt") as f:
        for word in f:
            word = word.strip().upper()
            dictionary.add(word)
            for i in range(len(word)):
                stems.add(word[: i + 1])
    return dictionary, stems


def create_grid_from_input(input_string):
    """
    Create a grid dictionary from an input string.
    Each comma in the input string separates rows, and each character in a row represents a cell in the grid.
    """
    rows = input_string.split(",")  # Split the input string into rows
    grid = {}
    for y, row in enumerate(rows):
        for x, letter in enumerate(row):
            grid[(x, y)] = letter.upper()  # Populate the grid dictionary
    return grid


def get_words():
    """Search each grid position and return all the words found"""
    for position in grid:
        logging.info(f"searching {position}")
        search([position])
    return [path_to_word(p) for p in paths]


def print_grid(grid):
    """Print the grid as a readable string"""
    s = ""
    for y in range(Y):
        for x in range(X):
            s += f"{grid[x, y]} "
        s += "\n"
    print(s)


def word_score(word):
    """Returns the boggle score for a given word"""
    wl = len(word)
    if wl < 3:
        return 0
    if wl in [3, 4]:
        return 1
    if wl == 5:
        return 2
    if wl == 6:
        return 3
    if wl == 7:
        return 5
    if wl >= 8:
        return 11


input_string = detected_grid
grid = create_grid_from_input(input_string)
size = X, Y = len(grid) // len(input_string.split(",")), len(input_string.split(","))

# size = X, Y = 4,
#
# 4
# grid = get_grid()
neighbours = get_neighbours()
dictionary, stems = get_dictionary()
paths = []
print_grid(grid)
words = get_words()
wordset = set(words)
totalwords = len(wordset)

sorted_words = sorted(wordset, key=lambda word: (len(word), word))

print(f"Found {totalwords} words:")
print(" Word\tPoints")
print("--------------")
for item in sorted_words:
    print(f"{item}\t{word_score(item)}")

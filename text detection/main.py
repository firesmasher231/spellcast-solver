import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import time


## manual loading


## manual loading

time.sleep(1)

import pyautogui

location = pyautogui.locateOnScreen(
    "C:/Users/asjos/Downloads/boggl/text detection/locate7.png", confidence=0.9
)

locationBot = pyautogui.locateOnScreen(
    "C:/Users/asjos/Downloads/boggl/text detection/locatebot7.png", confidence=0.9
)

# location = pyautogui.locateOnScreen(
#     "E:/Projects/spellcast-solver/text detection/locate.png", confidence=0.9
# )

# locationBot = pyautogui.locateOnScreen(
#     "E:/Projects/spellcast-solver/text detection/locatebot.png", confidence=0.9
# )


pyautogui.moveTo(
    location.left + location.width, location.top + location.height, duration=1
)

## auto capture

import mss.tools

# The screen part to capture  is from (location.left + location.width, location.top + location.height) to (locationBot.left, locationBot.top)

top_left = location.left + location.width
top_right = location.top + location.height

bottom_left = locationBot.left
bottom_right = locationBot.top

with mss.mss() as sct:
    # The screen part to capture
    monitor = {
        "top": int(top_right),
        "left": int(top_left),
        "width": int(bottom_left - top_left),
        "height": int(bottom_right - top_right),
    }
    output = "autoss.png".format(**monitor)

    print(monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    ## save sct_img to file

    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)

    img = cv2.imread(output)


# import mss.tools

# with mss.mss() as sct:
#     # The screen part to capture
#     monitor = {"top": 400, "left": 1000, "width": 550, "height": 550}
#     output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

#     # Grab the data
#     sct_img = sct.grab(monitor)

#     ## save sct_img to file

#     mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
#     print(output)

#     img = cv2.imread(output)


## end auto capture

# # read static image
# image_path = "C:/Users/asjos/Downloads/boggl/text detection/bog2.png"
# image_path = "E:/Projects/spellcast-solver/text detection/bog2.png"

# img = cv2.imread(image_path)

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
detected_centres = []


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
            ## append centre of bbox to detected_centres
            x = (bbox[0][0] + bbox[2][0]) / 2
            y = (bbox[0][1] + bbox[2][1]) / 2
            detected_centres.append((x, y))

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

    # for i in detected_letters:
    #     if len(i) != 1:
    #         detected_letters.remove(i)

    print(detected_letters, len(detected_letters))

    if len(detected_letters) == 25:
        break

    # split detected letters into 5x5 grid into format of "IAAYS,TYWDG,BDDTI,CPANO,MAIDN"


if len(detected_letters) != 25:
    print("Error: Detected letters are not 25")
    exit()

# zip togther detected_letters and detected_centres into tuple
zipped = list(zip(detected_letters, detected_centres))
print("zipped:", zipped)

# break zipped into 5x5 grid

original_grid = []

detected_grid = ""

for i in range(0, 25, 5):
    detected_grid += "".join(detected_letters[i : i + 5]) + ","
    original_grid.append(zipped[i : i + 5])

detected_grid = detected_grid[:-1]
print(detected_grid)

print("original grid:", original_grid)


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
        # print("word:", word, "path:", path)
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
    all_words = []
    """Search each grid position and return all the words found"""
    for position in grid:
        logging.info(f"searching {position}")
        search([position])
    # return [path_to_word(p) for p in paths]
    for p in paths:
        word = path_to_word(p)
        all_words.append((word, tuple(p)))  # Convert path list to tuple

    return all_words


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

# Sort the wordset based on the word length and then alphabetically
sorted_words = sorted(wordset, key=lambda word_path: (len(word_path[0]), word_path[0]))

print(f"Found {totalwords} words:")
print(" Word\tPoints")
print("--------------")
for word, path in sorted_words:
    print(f"{word}\t{word_score(word)}\t{path}")


def get_letter_and_coords(position, grid, original_data):
    # Check if the position exists in the grid
    if position not in grid:
        print(f"No letter found at grid position {position}.")
        return None, None

    # Get the letter from the specified grid position
    grid_letter = grid[position]

    # Create a mapping of letters to their occurrences and coordinates in original_data
    letter_occurrences = {}
    for row in original_data:
        for letter, coords in row:
            if letter not in letter_occurrences:
                letter_occurrences[letter] = []
            letter_occurrences[letter].append(coords)

    # Track the occurrence of the current letter in the grid
    current_occurrence = -1
    for y in range(len(original_data)):
        for x in range(len(original_data[y])):
            if grid[(x, y)] == grid_letter:
                current_occurrence += 1
                if (x, y) == position:
                    # Found the matching occurrence, get the original coordinates
                    if current_occurrence < len(letter_occurrences[grid_letter]):
                        original_coords = letter_occurrences[grid_letter][
                            current_occurrence
                        ]
                        return grid_letter, original_coords
                    else:
                        print(
                            f"Error: Mismatch in occurrences of letter '{grid_letter}' between grid and original data."
                        )
                        return None, None

    # If we reach here, something went wrong
    print(
        f"Letter '{grid_letter}' at grid position {position} was not found in the original data."
    )
    return None, None


# sorted_words = sorted(wordset, key=lambda word: (len(word), word))

# print(f"Found {totalwords} words:")
# print(" Word\tPoints")
# print("--------------")
# for item in sorted_words:
#     print(f"{item}\t{word_score(item)}")

# get the longest word

longest_word = sorted_words[-1]
print("longest word:", longest_word)

longest_path = longest_word[1]
print("longest word path:", longest_path)

coord_path = []

for position in longest_path:
    letter, coords = get_letter_and_coords(position, grid, original_grid)
    print(f"Letter: {letter}, Coords: {coords}")
    coord_path.append(coords)
print(coord_path)

import pyautogui

first = True

# pyautogui.moveTo(top_right, duration=0.5)
# print("moving to top right")
# time.sleep(3)

# pyautogui.moveTo(top_left, duration=0.5)
# print("moving to top left")
# time.sleep(3)

# pyautogui.moveTo(bottom_left, duration=0.5)
# print("moving to bottom left")
# time.sleep(3)

# pyautogui.moveTo(bottom_right, duration=0.5)
# print("moving to bottom right")
# time.sleep(3)


for coords in coord_path:

    x = coords[0] + location.left + location.width
    y = coords[1] + location.top + location.height

    print(
        "top_left:",
        top_left,
        "top_right:",
        top_right,
        "bottom_left:",
        bottom_left,
        "bottom_right:",
        bottom_right,
    )

    if first:
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.mouseDown(button="left")
        first = False
    else:
        pyautogui.moveTo(x, y, duration=0.5)

pyautogui.mouseUp(button="left")

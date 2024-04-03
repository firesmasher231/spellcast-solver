a = [
    [
        ("A", (57, 57)),
        ("Y", (167, 58)),
        ("R", (280, 58)),
        ("U", (387, 57)),
        ("O", (498, 57)),
    ],
    [
        ("L", (58, 167)),
        ("J", (166, 168)),
        ("A", (278, 166)),
        ("O", (387, 167)),
        ("I", (499, 168)),
    ],
    [
        ("E", (57, 276)),
        ("T", (168, 277)),
        ("N", (280, 276)),
        ("F", (390, 276)),
        ("Q", (498, 280)),
    ],
    [
        ("E", (57, 386)),
        ("T", (168, 387)),
        ("I", (278, 386)),
        ("N", (390, 386)),
        ("A", (499, 386)),
    ],
    [
        ("R", (60, 495)),
        ("O", (167, 495)),
        ("A", (278, 494)),
        ("A", (389, 494)),
        ("T", (499, 496)),
    ],
]

detected_grid = a
print(detected_grid)

# print as 5x5 grid

for i in range(5):
    row = ""
    for letter, (x, y) in detected_grid[i]:
        row += letter
    print(row)


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
    print(rows, "rows")
    grid = {}
    for y, row in enumerate(rows):
        print(row, "RRRRRow")
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
# size = X, Y = len(grid) // len(input_string.split(",")), len(input_string.split(","))
size = X, Y = 5, 5

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

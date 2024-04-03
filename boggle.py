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


def get_grid():
    """Return a dictionary of grid positions to random letters"""
    dice = {
        "0": ["R", "I", "F", "O", "B", "X"],
        "1": ["I", "F", "E", "H", "E", "Y"],
        "2": ["D", "E", "N", "O", "W", "S"],
        "3": ["U", "T", "O", "K", "N", "D"],
        "4": ["H", "M", "S", "R", "O", "W"],
        "5": ["L", "U", "P", "E", "T", "S"],
        "6": ["A", "C", "I", "T", "O", "A"],
        "7": ["Y", "L", "G", "K", "U", "E"],
        "8": ["E", "H", "I", "S", "P", "N"],
        "9": ["QU", "B", "M", "J", "O", "A"],
        "10": ["V", "E", "T", "I", "G", "N"],
        "11": ["B", "A", "L", "I", "Y", "T"],
        "12": ["E", "Z", "A", "V", "N", "D"],
        "13": ["R", "A", "L", "E", "S", "C"],
        "14": ["U", "W", "I", "L", "R", "G"],
        "15": ["P", "A", "C", "E", "M", "D"],
    }
    spent_dice = []

    def get_die():
        while True:
            thisdie = choice(range(16))
            if thisdie not in spent_dice:
                spent_dice.append(thisdie)
                return thisdie

    def get_face(die_number):
        return choice(dice[str(die_number)])

    return {(x, y): get_face(get_die()) for x in range(X) for y in range(Y)}


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


input_string = "IAYS,TYDG,BDDI,CPNO"
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


# from random import choice
# from string import ascii_uppercase
# import logging
# import time


# def timeit(method):
#     """Calculates time taken to run a function when called"""
#     def timed(*args, **kw):
#         t1 = time.time()
#         result = method(*args, **kw)
#         print '%r %2.2f sec' % (method.__name__, time.time() -t1)
#         return result

#     return timed


# def get_grid():
#     """Return a dictionary of grid positions to random letters"""
#     dice = {}
#     dice['0'] = ['R','I','F','O','B','X']
#     dice['1'] = ['I','F','E','H','E','Y']
#     dice['2'] = ['D','E','N','O','W','S']
#     dice['3'] = ['U','T','O','K','N','D']
#     dice['4'] = ['H','M','S','R','O','W']
#     dice['5'] = ['L','U','P','E','T','S']
#     dice['6'] = ['A','C','I','T','O','A']
#     dice['7'] = ['Y','L','G','K','U','E']
#     dice['8'] = ['E','H','I','S','P','N']
#     dice['9'] = ['QU','B','M','J','O','A']
#     dice['10'] = ['V','E','T','I','G','N']
#     dice['11'] = ['B','A','L','I','Y','T']
#     dice['12'] = ['E','Z','A','V','N','D']
#     dice['13'] = ['R','A','L','E','S','C']
#     dice['14'] = ['U','W','I','L','R','G']
#     dice['15'] = ['P','A','C','E','M','D']
#     spent_dice = []
#     def get_die():
#         found = 0
#         thisdie = 0
#         while found < 1:
#             thisdie = choice(range(0,16))
#             if thisdie not in spent_dice:
#                 found = 1
#                 spent_dice.append(thisdie)
#         return thisdie
#     def get_face(die_number):
#         face_label = choice(dice[str(die_number)])
#         return face_label
#     return {(x, y): get_face(get_die()) for x in range(X) for y in range(Y)}

# def get_neighbours():
#     """Return a dictionary with all the neighbours surrounding a particular position"""
#     neighbours = {}

#     for position in grid:
#         x, y = position
#         positions = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
#                      (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
#         neighbours[position] = [p for p in positions if 0 <= p[0] < X and 0 <= p[1] < Y]
#     return neighbours


# def path_to_word(path):
#     """Convert a list of grid positions to a word"""
#     return ''.join([grid[p] for p in path])


# def search(path):
#     """Recursively search the grid for words"""
#     word = path_to_word(path)
#     logging.debug('%s: %s' % (path, word))
#     if word not in stems:
#         return
#     if word in dictionary:
#         paths.append(path)
#     for next_pos in neighbours[path[-1]]:
#         if next_pos not in path:
#             search(path + [next_pos])
#         else:
#             logging.debug('skipping %s because in path' % grid[next_pos])

# def get_dictionary():
#     """Return a list of uppercase english words, including word stems"""
#     stems, dictionary = set(), set()
#     with open('words.txt') as f:
#         for word in f:
#             word = word.strip().upper()
#             dictionary.add(word)

#             for i in range(len(word)):
#                 stems.add(word[:i + 1])

#     return dictionary, stems


# def get_words():
#     """Search each grid position and return all the words found"""
#     for position in grid:
#         logging.info('searching %s' % str(position))
#         search([position])
#     return [path_to_word(p) for p in paths]


# def print_grid(grid):
#     """Print the grid as a readable string"""
#     s = ''
#     for y in range(Y):
#         for x in range(X):
#             s += grid[x, y] + ' '
#         s += '\n'
#     print s

# def word_score(word):
#     """Returns the boggle score for a given word"""
#     wl = len(word)
#     if wl < 3:
#         return 0
#     if ((wl == 3) or (wl == 4)):
#         return 1
#     if wl == 5:
#         return 2
#     if wl == 6:
#         return 3
#     if wl == 7:
#         return 5
#     if wl >= 8:
#         return 11

# size = X, Y = 4, 4
# grid = get_grid()
# neighbours = get_neighbours()
# dictionary, stems = get_dictionary()
# paths = []
# print_grid(grid)
# words = get_words()
# wordset = set(words)
# totalwords = len(wordset)

# print "Found "+str(totalwords) + " words:"
# print " Word\tPoints"
# print "--------------"
# for item in sorted(wordset):
#     print item+"\t"+str(word_score(item))

original_data = [
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


zipped = [
    [
        ("A", (57.5, 57.5)),
        ("Y", (167.5, 58.0)),
        ("R", (280.0, 58.0)),
        ("U", (387.5, 57.5)),
        ("O", (498.5, 57.5)),
    ],
    [
        ("L", (58.0, 167.0)),
        ("J", (166.0, 168.5)),
        ("A", (278.5, 166.5)),
        ("O", (387.5, 167.0)),
        ("I", (499.0, 168.0)),
    ],
    [
        ("E", (57.5, 276.5)),
        ("T", (168.0, 277.5)),
        ("N", (280.0, 276.5)),
        ("F", (390.5, 276.5)),
        ("Q", (498.5, 280.5)),
    ],
    [
        ("E", (57.5, 386.0)),
        ("T", (168.0, 387.5)),
        ("I", (278.0, 386.5)),
        ("N", (390.0, 386.5)),
        ("A", (499.5, 386.0)),
    ],
    [
        ("R", (60.0, 495.5)),
        ("O", (167.5, 495.5)),
        ("A", (278.5, 494.5)),
        ("A", (389.0, 494.5)),
        ("T", (499.5, 496.5)),
    ],
]

data = {
    (0, 0): ("A", (57, 57)),
    (1, 0): ("Y", (167, 58)),
    (2, 0): ("R", (280, 58)),
    (3, 0): ("U", (387, 57)),
    (4, 0): ("O", (498, 57)),
    (0, 1): ("L", (58, 167)),
    (1, 1): ("J", (166, 168)),
    (2, 1): ("A", (278, 166)),
    (3, 1): ("O", (387, 167)),
    (4, 1): ("I", (499, 168)),
    (0, 2): ("E", (57, 276)),
    (1, 2): ("T", (168, 277)),
    (2, 2): ("N", (280, 276)),
    (3, 2): ("F", (390, 276)),
    (4, 2): ("Q", (498, 280)),
    (0, 3): ("E", (57, 386)),
    (1, 3): ("T", (168, 387)),
    (2, 3): ("I", (278, 386)),
    (3, 3): ("N", (390, 386)),
    (4, 3): ("A", (499, 386)),
    (0, 4): ("R", (60, 495)),
    (1, 4): ("O", (167, 495)),
    (2, 4): ("A", (278, 494)),
    (3, 4): ("A", (389, 494)),
    (4, 4): ("T", (499, 496)),
}

grid = {
    (0, 0): "A",
    (1, 0): "Y",
    (2, 0): "R",
    (3, 0): "U",
    (4, 0): "O",
    (0, 1): "L",
    (1, 1): "J",
    (2, 1): "A",
    (3, 1): "O",
    (4, 1): "I",
    (0, 2): "E",
    (1, 2): "T",
    (2, 2): "N",
    (3, 2): "F",
    (4, 2): "Q",
    (0, 3): "E",
    (1, 3): "T",
    (2, 3): "I",
    (3, 3): "N",
    (4, 3): "A",
    (0, 4): "R",
    (1, 4): "O",
    (2, 4): "A",
    (3, 4): "A",
    (4, 4): "T",
}


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


# # Example usage:
# position_to_search = (4, 2)  # This is the grid position you're interested in
# letter, coords = get_letter_and_coords(position_to_search, grid, original_data)
# if letter and coords:
#     print(
#         f"Letter '{letter}' at grid position {position_to_search} maps to original coordinates {coords}."
#     )
# else:
#     print("Could not find the original coordinates for the specified position.")


# Sample grid and original data
sample_word = ((2, 3), (3, 3), (3, 2), (2, 1), (2, 2), (1, 3), (0, 2), (0, 3), (0, 4))

coord_path = []

for position in sample_word:
    letter, coords = get_letter_and_coords(position, grid, original_data)
    print(f"Letter: {letter}, Coords: {coords}")
    coord_path.append(coords)
print(coord_path)

import pyautogui

first = True

for coords in coord_path:
    if first:
        pyautogui.moveTo(coords, duration=0.5)
        pyautogui.mouseDown(button="left")
        first = False
    else:
        pyautogui.moveTo(coords, duration=0.5)

pyautogui.mouseUp(button="left")

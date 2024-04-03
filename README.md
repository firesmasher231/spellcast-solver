# Spellcast Solver 🧙‍♂️✨

Its no fun when friends are better than you at games, welcome to Spellcast Solver, your tool for dominating the word game "Spellcast" on Discord.

## What's Inside? 📦

Spellcast Solver uses a concoption of image capture and OCR (Optical Character Recognition) to automatically solve puzzles by detecting letters and generating words. It's a very janky solution for when you're looking to outsmart your friends at Spellcast - all in good fun, of course!

### Features

- **Automatic Screenshot Capture**: Grabs the game screen directly from your monitor. (adjust the screenshot location thru a lot of trial and error)
- **Letter Detection**: Uses `easyocr` to detect letters on the game screen. ( works all the time, most of the time)
- **Word Generation**: Crunches those letters to find possible words using a custom algorithm and a touch of magic. ( this actually works pretty well)
- **Boggle Scoring**: Not just any words, but the ones that score you points in Spellcast. 

### Tech Stack

- Python 🐍
- `cv2` for image processing
- `easyocr` for character recognition
- `matplotlib` and `numpy` for handling and visualizing data
- `mss` for screen capture

## Getting Started 🚀

1. **Clone this repository:**

   ```bash
   git clone https://github.com/yourusername/spellcast-solver.git
   ```

2. **Install dependencies:**

   Make sure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Solver:**

   Simply execute the script while playing Spellcast on Discord:

   ```bash
   python spellcast_solver.py
   ```

4. **Enjoy your newfound power** (responsibly) 😉

## How It Works 🧠

The script captures a portion of your screen where the game is displayed, detects letters using OCR, and then processes these letters to find all possible words. It's like having a spellbook that automatically flips to the right page!

## Contributing 🤝

Got ideas on how to make Spellcast Solver even better? Contributions are welcome! Whether it's improving the algorithm, adding new features, or fixing bugs, feel free to fork this repo and send over a pull request.

## Disclaimer 📜

This tool is meant for educational purposes and to have a laugh with friends. Please use it responsibly and keep the spirit of the game alive!

Parts of this readme was very much chatgpt generated 🙌

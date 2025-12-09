# Cursor-First-Test-Project-

An exploratory project to test, learn and utilise cursor for projects in terms of app and web development

## Keyboard Piano Project

This project contains an interactive keyboard piano that plays musical notes when you press keys on your keyboard.

### Features

- **Interactive Mode**: Press keys on your keyboard to play musical notes in real-time
- **Auto-Play Mode**: Automatically plays the song sequence you provided
- Maps keyboard keys to musical notes (D, F, G, A, E, B, C5)

### Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

**Note:** This version uses `pynput` instead of `pygame` to work with Python 3.13+. On Windows, audio playback uses the built-in `winsound` module, so no additional audio libraries are required!

### Usage

Run the script:

```bash
python keyboard_piano.py
```

You'll be presented with options:

1. **Play the song sequence automatically** - Plays the entire song pattern you provided
2. **Interactive mode** - Press keys on your keyboard to play notes in real-time
3. **Exit** - Close the program

### Key Mappings

The computer keyboard is mapped 1-to-1 to a piano keyboard, starting from the
letter **A** as the first white key:

- **White keys (bottom row)**

  - `A` → C
  - `S` → D
  - `D` → E
  - `F` → F
  - `G` → G
  - `H` → A
  - `J` → B
  - `K` → C5
  - `L` → D5
  - `;` → E5
  - `'` → F5

- **Black keys (top row)**

  - `W` → C#
  - `E` → D#
  - `T` → F#
  - `Y` → G#
  - `U` → A#
  - `O` → C#5
  - `P` → D#5

- **Other**
  - `Enter` → Rest/pause

### Song Identification

The pattern you provided appears to be a melody that can be played using these keyboard mappings. The script allows you to both:

- Play it automatically to hear the full song
- Play it interactively by pressing the keys yourself

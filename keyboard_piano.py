"""
Interactive Keyboard Piano
Play musical notes by pressing keys on your keyboard.
This version works with Python 3.13+ (no pygame required).
"""

import sys
import time
import math
import wave
import tempfile
import os
from pynput import keyboard

# Musical note frequencies (in Hz) - C4 to F5 range
NOTE_FREQUENCIES = {
    'C': 261.63,  # C4
    'C#': 277.18, # C#4/Db4
    'D': 293.66,  # D4
    'D#': 311.13, # D#4/Eb4
    'E': 329.63,  # E4
    'F': 349.23,  # F4
    'F#': 369.99, # F#4/Gb4
    'G': 392.00,  # G4
    'G#': 415.30, # G#4/Ab4
    'A': 440.00,  # A4
    'A#': 466.16, # A#4/Bb4
    'B': 493.88,  # B4
    'C5': 523.25, # C5
    'C#5': 554.37,# C#5/Db5
    'D5': 587.33, # D5
    'D#5': 622.25,# D#5/Eb5
    'E5': 659.25, # E5
    'F5': 698.46, # F5
}

# Map keyboard keys to actual musical notes (Piano keyboard layout)
# 1-to-1 mapping starting from the letter A on the keyboard.
# Bottom row letters (A S D F G H J K L ; '):
#   A  S  D  F  G  H  J  K   L   ;   '
#   C  D  E  F  G  A  B  C5 D5  E5  F5
#
# Top row letters for black keys (W E T Y U O P):
#   W   E   T   Y   U   O    P
#   C#  D#  F#  G#  A#  C#5  D#5
KEY_NOTE_MAP = {
    # White keys - bottom row
    'a': 'C',     # A key = C
    's': 'D',     # S key = D
    'd': 'E',     # D key = E
    'f': 'F',     # F key = F
    'g': 'G',     # G key = G
    'h': 'A',     # H key = A
    'j': 'B',     # J key = B
    'k': 'C5',    # K key = C5
    'l': 'D5',    # L key = D5
    ';': 'E5',    # ; key = E5
    "'": 'F5',    # ' key = F5

    # Black keys - top row
    'w': 'C#',    # W key = C#
    'e': 'D#',    # E key = D#
    't': 'F#',    # T key = F#
    'y': 'G#',    # Y key = G#
    'u': 'A#',    # U key = A#
    'o': 'C#5',   # O key = C#5
    'p': 'D#5',   # P key = D#5

    # Other controls
    '\r': None,   # Enter key (pause/rest)
}

def generate_tone_samples(frequency, duration=0.3, sample_rate=44100):
    """Generate audio samples for a sine wave tone."""
    frames = int(duration * sample_rate)
    max_amplitude = 32767  # Maximum value for 16-bit signed integer
    
    # Generate sine wave samples
    samples = []
    for i in range(frames):
        sample = max_amplitude * math.sin(2.0 * math.pi * frequency * i / sample_rate)
        samples.append(int(sample))
    
    return samples

def generate_tone_wav(frequency, duration=0.3, sample_rate=44100):
    """Generate a WAV file with a sine wave tone."""
    samples = generate_tone_samples(frequency, duration, sample_rate)
    
    # Create temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_file.close()
    
    # Write WAV file
    with wave.open(temp_file.name, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        # Convert samples to bytes (little-endian 16-bit)
        frames_bytes = b''.join([int(s).to_bytes(2, byteorder='little', signed=True) for s in samples])
        wav_file.writeframes(frames_bytes)
    
    return temp_file.name

def play_note(note_name, duration=0.3):
    """Play a musical note by name."""
    if note_name is None:
        time.sleep(duration)
        return
    
    if note_name in NOTE_FREQUENCIES:
        frequency = NOTE_FREQUENCIES[note_name]
    else:
        print(f"Unknown note: {note_name}")
        return
    
    try:
        # Try using winsound (Windows built-in)
        import winsound
        # winsound.Beep only works with integer frequencies (37-32767 Hz)
        freq_int = int(frequency)
        if 37 <= freq_int <= 32767:
            winsound.Beep(freq_int, int(duration * 1000))
        else:
            # Fallback: generate WAV and play
            wav_file = generate_tone_wav(frequency, duration)
            winsound.PlaySound(wav_file, winsound.SND_FILENAME | winsound.SND_NOSTOP)
            time.sleep(duration)
            os.unlink(wav_file)
    except ImportError:
        # For non-Windows systems, try sounddevice or pydub
        try:
            import sounddevice as sd
            import numpy as np
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = np.sin(2 * np.pi * frequency * t)
            sd.play(wave, sample_rate)
            sd.wait()
        except ImportError:
            # Last resort: print the note
            print(f"Playing note: {note_name} ({frequency} Hz) - Install sounddevice for audio")
            time.sleep(duration)
    except Exception as e:
        print(f"Error playing note {note_name}: {e}")

def generate_audio_file(sequence, output_filename="song_output.wav", note_duration=0.22, sample_rate=44100):
    """Generate a WAV file from the song sequence.

    This version:
    - Plays the full sequence **twice** (2 loops)
    - Uses a slightly shorter note duration for a faster tempo
    """
    print(f"\nGenerating audio file: {output_filename}")
    print("This may take a moment...")
    
    all_samples = []
    note_count = 0

    # Play the sequence twice (2 loops)
    for loop in range(2):
        print(f"  Processing loop {loop + 1}/2...")
        for char in sequence:
            if char.lower() in KEY_NOTE_MAP:
                note = KEY_NOTE_MAP[char.lower()]
                if note:
                    # Generate samples for this note
                    frequency = NOTE_FREQUENCIES[note]
                    samples = generate_tone_samples(frequency, note_duration, sample_rate)
                    all_samples.extend(samples)
                    note_count += 1
                    if note_count % 10 == 0:
                        print(f"  Processed {note_count} notes...")
                else:
                    # Rest/silence (Enter key)
                    silence_frames = int(note_duration * sample_rate)
                    all_samples.extend([0] * silence_frames)
            elif char == ' ':
                # Short pause for spaces (scaled slightly faster)
                silence_frames = int(0.08 * sample_rate)
                all_samples.extend([0] * silence_frames)
            elif char == '\n':
                # Pause for newlines (scaled slightly faster)
                silence_frames = int(0.18 * sample_rate)
                all_samples.extend([0] * silence_frames)
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_filename)
    
    # Write WAV file
    print(f"  Writing {len(all_samples)} samples to file...")
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        # Convert samples to bytes (little-endian 16-bit)
        frames_bytes = b''.join([int(s).to_bytes(2, byteorder='little', signed=True) for s in all_samples])
        wav_file.writeframes(frames_bytes)
    
    file_size = os.path.getsize(output_path)
    duration = len(all_samples) / sample_rate
    print(f"\n✓ Audio file saved successfully!")
    print(f"  File: {output_path}")
    print(f"  Size: {file_size / 1024:.2f} KB")
    print(f"  Duration: {duration:.2f} seconds")
    print(f"  Notes: {note_count}")
    
    return output_path

def play_sequence(sequence):
    """Play a sequence of notes from the song pattern."""
    print("\nPlaying sequence...")
    for char in sequence:
        if char.lower() in KEY_NOTE_MAP:
            note = KEY_NOTE_MAP[char.lower()]
            if note:
                print(f"Playing: {char} -> {note}")
                play_note(note, duration=0.3)
            else:
                print("Rest (Enter key)")
                time.sleep(0.3)
        elif char == ' ':
            time.sleep(0.1)  # Short pause for spaces
        elif char == '\n':
            time.sleep(0.2)  # Pause for newlines
        else:
            print(f"Unknown key: {char}")

def on_press(key):
    """Handle key press events."""
    try:
        # Get the character representation of the key
        if hasattr(key, 'char') and key.char:
            key_char = key.char.lower()
        else:
            # Handle special keys
            if key == keyboard.Key.enter:
                key_char = '\r'
            elif key == keyboard.Key.esc:
                print("\nExiting interactive mode...")
                return False  # Stop listener
            else:
                return  # Ignore other special keys
        
        if key_char in KEY_NOTE_MAP:
            note = KEY_NOTE_MAP[key_char]
            if note:
                print(f"Key '{key_char}' -> Note: {note}")
                play_note(note, duration=0.3)
    except AttributeError:
        pass

def interactive_mode():
    """Interactive mode: play notes when keys are pressed."""
    print("\n" + "="*60)
    print("INTERACTIVE KEYBOARD PIANO MODE")
    print("="*60)
    print("Piano Keyboard Layout (1-to-1 from letter A):")
    print("\nWhite Keys (bottom row):")
    print("  A -> C    S -> D    D -> E    F -> F")
    print("  G -> G    H -> A    J -> B    K -> C5")
    print("  L -> D5   ; -> E5   ' -> F5")
    print("\nBlack Keys (top row):")
    print("  W -> C#   E -> D#   T -> F#   Y -> G#")
    print("  U -> A#   O -> C#5  P -> D#5")
    print("\nOther:")
    print("  Enter -> Rest/Pause")
    print("\nPress ESC to exit")
    print("="*60 + "\n")
    
    # Start keyboard listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def main():
    """Main function."""
    # The song sequence from the user
    song_sequence = """D F G H G T G H K ; G

; ; L K H 

H J K L K H U J 

J K J G Y H 

U J K L ; L K J H L 

D F G H G T G H K ; G 

; ; L K H 

H J K L K J K J 

H Y G H K ; \r

G H ' J K"""
    
    print("="*60)
    print("KEYBOARD PIANO - Song Player")
    print("="*60)
    print("\nChoose an option:")
    print("1. Play the song sequence automatically")
    print("2. Interactive mode (press keys to play notes)")
    print("3. Save song as audio file (WAV)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1/2/3/4): ").strip()
    
    if choice == '1':
        play_sequence(song_sequence)
    elif choice == '2':
        interactive_mode()
    elif choice == '3':
        filename = input("Enter filename (default: song_output.wav): ").strip()
        if not filename:
            filename = "song_output.wav"
        if not filename.endswith('.wav'):
            filename += '.wav'
        generate_audio_file(song_sequence, filename)
    elif choice == '4':
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

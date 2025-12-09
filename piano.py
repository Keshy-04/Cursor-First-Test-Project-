import pygame 
import numpy as np 
import time

pygame.init()

pygame.mixer.init(frequency=44100, size=-16, channels=2)

SAMPLE_RATE = 44100
DURATION = 0.5
NOTE_DURATION = 0.3  # Duration for each note in the sequence

def generate_tone(frequency, duration=DURATION, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    audio = np.int16(wave * 32767)

    audio_stereo = np.column_stack([audio, audio])

    return pygame.sndarray.make_sound(audio_stereo)

key_freq_map = {
    pygame.K_a: 261.63,
    pygame.K_s: 293.66,
    pygame.K_d: 329.63,
    pygame.K_f: 349.23,
    pygame.K_g: 392.00,
    pygame.K_h: 440.00,
    pygame.K_j: 493.88,
    pygame.K_k: 523.25,
    pygame.K_l: 587.33,
    ord(';'): 659.25,  # Semicolon key using ord()
    ord("'"): 698.46,  # Quote/apostrophe key using ord()

    pygame.K_RETURN: 783.99,
    pygame.K_w: 277.18,
    pygame.K_e: 311.13,
    pygame.K_t: 369.99,
    pygame.K_y: 415.30,
    pygame.K_u: 466.16,
    pygame.K_o: 554.37,
    pygame.K_p: 622.25,
    pygame.K_LEFTBRACKET: 739.99,
    pygame.K_RIGHTBRACKET: 783.99,
}

sounds = {key: generate_tone(freq) for key, freq in key_freq_map.items()}
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Keyboard Piano")

# Map script characters to pygame key codes
def char_to_key(char):
    """Convert script character to pygame key code."""
    char_map = {
        'D': pygame.K_d,
        'F': pygame.K_f,
        'G': pygame.K_g,
        'H': pygame.K_h,
        'T': pygame.K_t,
        'K': pygame.K_k,
        ';': ord(';'),
        'L': pygame.K_l,
        'J': pygame.K_j,
        'Y': pygame.K_y,
        'U': pygame.K_u,
        "'": ord("'"),
        '\r': pygame.K_RETURN,  # Enter key
    }
    return char_map.get(char.upper() if char.isalpha() else char)

# The song sequence
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

def play_sequence():
    """Automatically play the song sequence."""
    print("Playing song sequence...")
    print("Press ESC to skip or close window to exit")
    
    for char in song_sequence:
        # Handle pygame events to keep window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Sequence interrupted by user")
                    return False
        
        if char == ' ':
            # Short pause for spaces
            time.sleep(0.1)
        elif char == '\n':
            # Pause for newlines
            time.sleep(0.2)
        else:
            key = char_to_key(char)
            if key and key in sounds:
                sounds[key].play()
                time.sleep(NOTE_DURATION)
            elif key == pygame.K_RETURN:
                # Rest/pause for Enter key
                time.sleep(NOTE_DURATION)
    
    print("Sequence finished!")
    return True

# Auto-play the sequence when program starts
play_sequence()

# After sequence, allow interactive mode
running = True
print("\nInteractive mode - Press keys to play notes, ESC to exit")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in sounds:
                sounds[event.key].play()

pygame.quit()

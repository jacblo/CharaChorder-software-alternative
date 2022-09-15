from pynput import keyboard
from pynput.keyboard import Key, Controller

controller = Controller()

def on_chord(chord, last_space): # dummy function to be replaced
    print(chord)
    return True

keys_down = 0
keys_pressed = []
last_space = False
soft_end = True

def on_press(key):
    global keys_pressed, keys_down
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    keys_down += 1
    keys_pressed.append(k)


min_chord_length = 2

end_key = keyboard.Key.esc
end_key_modifier = "shift"

def on_release(key):
    global keys_pressed, keys_down, last_space, soft_end
    if key == end_key:
        if end_key_modifier in keys_pressed:
            print("stopped")
            soft_end = False
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    
    keys_down -= 1
    
    if key == keyboard.Key.space:
        if "space" in keys_pressed:
            keys_pressed.remove("space")
        if len(keys_pressed) >= min_chord_length:
            result = on_chord(keys_pressed, last_space)
            keys_pressed = []
            return result
    
    if len(keys_pressed) < min_chord_length:
        keys_pressed = []
    return True


def backspace(length):
    for i in range(length):
        controller.press(keyboard.Key.backspace)
        controller.release(keyboard.Key.backspace)

def write(text):
    controller.type(text)

def start():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()  # start to listen on a separate thread
    listener.join()

if __name__ == '__main__':
    start()  # remove if main thread is polling self.keys
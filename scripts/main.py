import utils
import json
import os

lang = 'en'
if not os.path.exists(f"languages/{lang}.json"):
    print("language pack not found")
    os._exit(1)

with open(f"languages/{lang}.json", 'r') as f:
    data = json.load(f)

letters = data["letters"]
dictionary = data["dictionary"]
print("data loaded")

def similarity(word, chord, pos = 0):
    if word == "".join(chord):
        print("written correctly")
        return float("inf")
    word = set(word)
    chord = set(chord)
    score = 0
    
    if word == chord:
        score += 100
    else:
        return float("-inf")
    
    score -= pos*2
    return score

def find_best(chord):
    global dictionary
    maximum = ""
    maximum_score = float("-inf")
    for i, word in enumerate(dictionary):
        score = similarity(word, chord, i)
        if score > maximum_score:
            maximum = word
            maximum_score = score
    
    return maximum

def replace_word(original_len, word):
    utils.backspace(original_len+1)
    utils.write(word+(" " if len(word) != 0 else ""))
    
def on_chord(chord, last_space):
    if not all(ch in letters for ch in chord):
        return True
    
    print(f"{''.join(chord)} V")
    word = find_best(chord)
    replace_word(len(chord), word)
    print(word)
    return True

utils.on_chord = on_chord
while utils.soft_end:
    print("started")
    utils.start()
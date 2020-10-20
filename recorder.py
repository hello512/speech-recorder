##  this scripts records audio samples as trainings data for my speech recognition ai.
##  the samples are stored as numpy arrays

from numpy import savez_compressed, load
import sounddevice as sd
import numpy as np
import random
import string
import time
import os

def load_words():
    with open("words.txt", "r") as word_file:
        return word_file.read().replace(" ", "").split(",")

WORDS = load_words()

seconds = 1
samplerate = 44100
letters = string.ascii_lowercase + string.ascii_uppercase
length = 32

def generate_name(word):
    random_name = "".join([random.choice(letters) for i in range(length)])
    try:
        names = os.listdir(f"data/{word}")
    except FileNotFoundError:
        os.mkdir(f"data/{word}")
    else:
        while random_name in names:
            random_name = "".join([random.sample(letters) for i in range(length)])
    return random_name


def save_data(word, data):
    savez_compressed(f"data/{word}/%s.npz" % generate_name(word), data)
    

while True:
    for word in WORDS:
        print(f"say: %s" % word)
        recorded_data = sd.rec(seconds * samplerate, samplerate = samplerate, channels = 1)
        sd.wait()
        print("recording finished")
        save_data(word, recorded_data)
        time.sleep(2)

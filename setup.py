import numpy as np
import csv
from config import color_csv, character_csv


emoji_color = np.genfromtxt(color_csv, delimiter=',')[:, 1:]

with open(character_csv, 'rb') as f:
	reader = csv.reader(f)
	emoji_character = list(reader)
emoji_character = [a[1].decode('utf8') for a in emoji_character]
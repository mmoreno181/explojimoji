import os
import csv


dir = '../emoji_data/fb'

with open('fb_emoji.csv', 'rb') as f:
    reader = csv.reader(f)
    links = list(reader)

filenames = os.listdir(dir)
for index, file in enumerate([f[0:-4] for f in filenames]):
    i, file = file.split('___')
    characters = file.split('_')
    out = u''
    for character in characters:
        out += '\U' + character.rjust(8, '0')
    print str(index)+','+out+','+links[int(i)][0]

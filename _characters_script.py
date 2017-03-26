import os
filenames = os.listdir('emojis/png_64_2')
for index, file in enumerate([f[0:-4] for f in filenames]):
    characters = file.split('-')
    out = u''
    for character in characters:
        out += '\U' + character.rjust(8, '0')
    print str(index)+','+out

import os
import urllib

dir = '../emoji_data/fb'
source = 'fb_emoji.txt'

with open(source, 'rb') as f:
    urls = f.readlines()
i = 0
for url in urls:
    filename = url.strip().split('/')[-1]
    
    if not '200d' in filename:
        urllib.urlretrieve(url, dir + '/' + str(i) + '___' + filename)
    i+=1

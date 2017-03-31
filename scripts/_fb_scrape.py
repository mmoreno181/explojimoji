import os
import urllib

with open('fb_emoji.txt', 'rb') as f:
    urls = f.readlines()
for url in urls:
    urllib.urlretrieve(url, '../emoji_data/fb/{}'.format(url.strip().split('/')[-1]))


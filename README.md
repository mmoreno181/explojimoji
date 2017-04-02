# emoji_exploji


Emoji Exploji is a project created by Maria Moreno and Ryan Trad as a hackathon submission at HackEmory V. Maria and Ryan are undergraduate students at the Georgia Institute of Technology. 

This application takes in a png or bitmap image and uses Lloyd's algorithm to perform k-means clustering on that image. After the image pixels are divided into k clusters, we match an emoji character to each cluster based on the emoji's average pixel color. Before doing any clustering, we downscale the image in order to improve run-time.

## How to use:
pip install -r requirements.txt <br>
execute application.py

## Website
[Emoji Exploji Website](http://exploji.tk)


import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from scipy import misc
import sys, os

def flatten_image(image):
    n = image.shape[0] * image.shape[1]
    pixels = np.zeros((n, 3))
    pixels[:,0] = np.ndarray.flatten(image[:,:,0])
    pixels[:,1] = np.ndarray.flatten(image[:,:,1])
    pixels[:,2] = np.ndarray.flatten(image[:,:,2])
    return pixels

def cluster_pixels(pixels, k=10):
    n = pixels.shape[0]

    kmeans = KMeans(n_clusters=int(k)).fit(pixels)
    assignment = kmeans.labels_
    centroid = kmeans.cluster_centers_

    return assignment, centroid

def average_image_pixel(image):
    if image.shape[2] == 4:
        opaque_image = image[image[:,:,3]==255]
    elif image.shape[2] == 3:
        opaque_image = image[image[:,:,1]>=0]
    else:
        layer = image[image[:,:,0]>=0]
        opaque_image = np.concatenate((layer,layer,layer), axis=1)

    average = np.zeros((1,1,3))
    average[:,:,0] = np.mean(opaque_image[:,0])
    average[:,:,1] = np.mean(opaque_image[:,1])
    average[:,:,2] = np.mean(opaque_image[:,2])

    standard_dev = np.zeros(3)
    standard_dev[0] = np.std(opaque_image[:,0])
    standard_dev[1] = np.std(opaque_image[:,1])
    standard_dev[2] = np.std(opaque_image[:,2])

    return average, standard_dev

def assign_emoji_to_cluster(cluster_centroids, emoji_color, emoji_character):
    distance = np.zeros(emoji_color.shape[0])
    assigned_emoji = []
    for i in range(cluster_centroids.shape[0]):
        distance = cluster_centroids[i,:] - emoji_color[1]
        emoji_index = np.argmin(distance)
        assigned_emoji.append(emoji_character[emoji_index])
    return assigned_emoji

def reconstruct_image(assigned_emoji, original_image, assignment):
    rows = original_image.shape[0]
    cols = original_image.shape[1]
    new_image = []
    for i in range(rows*cols):
        new_image.append(assigned_emoji[assignment[i]])
    out_image = []
    for i in range(rows):
        out_image.append(new_image[i*cols: i*cols+cols])
    return out_image

def convert_image_to_emoji(filename, emoji_color, emoji_character, k=10):
    image = misc.imread(filename)
    flattened_image = flatten_image(image)
    assignment, centroids = cluster_pixels(flattened_image, k=k)
    assigned_emoji = assign_emoji_to_cluster(centroids, emoji_color, emoji_character)
    new_image = reconstruct_image(assigned_emoji, image, assignment)
    out_text = u""
    for row in new_image:
        # print row
        out_text += ' '.join(row) + '\n'
    return out_text

if __name__ == '__main__':
    convert_image_to_emoji(sys.argv[1], sys.argv[2], sys.argv[3])

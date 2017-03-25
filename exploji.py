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

def get_average_emoji_pixels(path):
    filenames = os.listdir(path)
    average_pixel_list = np.zeros((3, len(filenames)))
    stdev_pixel_list = np.zeros((3, len(filenames)))
    for i in range(len(filenames)):
        image = misc.imread(os.path.join(path, filenames[i]))
        print(filenames[i])
        average_pixel_list[:,i], stdev_pixel_list[:,i] = average_image_pixel(image)
    return average_pixel_list

def assign_emoji_to_cluster(cluster_centroids, average_emoji_pixel, emoji_data):
    distance = np.zeros(average_emoji_pixel.shape[0])
    assigned_emoji = []
    for i in range(cluster_centroids.shape[0]):
        distance = cluster_centroids[i,:] - average_emoji_pixel[1]
        emoji_index = argmin(distance)
        assigned_emoji.append(emoji_data[emoji_index]['unicode'])
    return assigned_emoji

def reconstruct_image(assigned_emoji, original_image):
    rows = original_image.shape[0]
    cols = original_image.shape[1]
    new_flat_image_row = [None] * rows
    new_flat_image = new_flat_image_row * cols
    for i in range(0,rows):
        for j in range(1,cols):
            new_flat_image[i][j] = assigned_emoji[assignment[(j - 1) * rows + i]]

def main(filename, average_emoji_pixel, emoji_data):
    image = misc.imread(filename)
    flattened_image = flatten_image(image)
    assignment, centroids = cluster_pixels(flattened_image)
    assigned_emoji = assign_emoji_to_cluster(centroids, average_emoji_pixel, emoji_data)
    new_image = reconstruct_image(assigned_emoji, image)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

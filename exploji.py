import numpy as np
from sklearn.cluster import KMeans
from scipy import misc

def flatten_image(image):
    n = image.shape[0] * image.shape[1]
    pixels = np.zeros((n, 3))
    pixels[:,0] = np.ndarray.flatten(image[:,:,0])
    pixels[:,1] = np.ndarray.flatten(image[:,:,1])
    pixels[:,2] = np.ndarray.flatten(image[:,:,2])
    return pixels

def cluster_pixels(pixels, k, centroids=None):
    n = pixels.shape[0]

    kmeans = KMeans(n_clusters=int(k)).fit(pixels)
    assignment = kmeans.labels_
    centroid = kmeans.cluster_centers_

    return assignment, centroid

def average_image_pixel(image):
    return np.mean(image, axis=0)

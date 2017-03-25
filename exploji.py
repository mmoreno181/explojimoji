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

def cluster_pixels(pixels, k, centroids=None):
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
        image = misc.imread(os.path.join('emojis/png_64', filenames[i]))
        print(filenames[i])
        average_pixel_list[:,i], stdev_pixel_list[:,i] = average_image_pixel(image)
    return average_pixel_list

def main(filename):
    print(get_average_emoji_pixels(filename))
    # image = misc.imread(filename)
    # average_pixel, stdev = average_image_pixel(image)
    # print average_pixel, stdev
    # color = np.zeros((1,1,3))
    # color[:,:,0] = 79
    # color[:,:,1] = 209
    # color[:,:,2] = 217
    #color = np.array([79., 209., 217.])

if __name__ == '__main__':
    main(sys.argv[1])

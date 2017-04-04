import os
import numpy as np
from scipy import misc

dir = '../emoji_data/fb'

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

filenames = os.listdir(dir)
stdev_pixel_list = np.zeros((3, len(filenames)))
for i in range(len(filenames)):
    image = misc.imread(os.path.join(dir, filenames[i]))
    average_pixel_list, stdev_pixel_list[:,i] = average_image_pixel(image)

    average_pixel_list = average_pixel_list[0][0].tolist()
    average_pixel_list.insert(0, i)
    print ','.join(str(x) for x in average_pixel_list)

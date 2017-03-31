import os
from exploji import average_image_pixel
import numpy as np
from scipy import misc

filenames = os.listdir('../emoji_data/png_64')
stdev_pixel_list = np.zeros((3, len(filenames)))
for i in range(len(filenames)):
    image = misc.imread(os.path.join('../emoji_data/png_64', filenames[i]))
    average_pixel_list, stdev_pixel_list[:,i] = average_image_pixel(image)

    average_pixel_list = average_pixel_list[0][0].tolist()
    average_pixel_list.insert(0, i)
    print ','.join(str(x) for x in average_pixel_list)
import os,glob

from os import listdir, makedirs
from os.path import isfile, join

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import cv2
import numpy as np

from PIL import Image

def main():
    path = "/home/martin/Data/Hard-Cases/RGB/" # Source Folder
    dstpath = "/home/martin/Data/Hard-Cases/Gray/" # Destination Folder
    try:
        makedirs(dstpath)
    except:
        print ("Directory already exist, images will be written in same folder")

    # Folder won't used
    files = list(filter(lambda f: isfile(join(path,f)), listdir(path)))

    for image in files:
        try:
            img = cv2.imread(os.path.join(path, image))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            dstPath = join(dstpath, image)
            cv2.imwrite(dstPath, gray)
        except:
            print ("{} is not converted".format(image))

    for fil in glob.glob("*.png"):
        try:
            image = cv2.imread(fil) 
            gray_image = cv2.cvtColor(os.path.join(path,image), \
                cv2.COLOR_BGR2GRAY) # convert to greyscale
            cv2.imwrite(os.path.join(dstpath, fil), gray_image)
        except:
            print('{} is not converted')

if __name__ == "__main__":
    main()

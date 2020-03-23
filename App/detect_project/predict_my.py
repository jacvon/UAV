#!/usr/bin/env python
# coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
import h5py
import scipy
from PIL import Image
from scipy import ndimage
#from App.lr_utils import load_dataset
import skimage
from App.detect_project.train import *
#my_image = "my_image2.jpg"  # change this to the name of your image file

#fname = "images/" + my_image


def func_predict(fname):
    image = np.array(plt.imread(fname))
    my_image = np.array(Image.fromarray(image).resize((num_px, num_px))).reshape((1, num_px * num_px * 3)).T
    my_predicted_image = predict(d["w"], d["b"], my_image)
    #print("y = " + str(np.squeeze(my_predicted_image)) + ", your algorithm predicts a \"" + classes[
    #    int(np.squeeze(my_predicted_image)),].decode("utf-8") + "\" picture.")
    my_predicted = int(np.squeeze(my_predicted_image))
    return my_predicted

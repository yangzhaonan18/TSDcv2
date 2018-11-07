import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from skimage.feature import blob_dog, blob_log, blob_doh
import imutils
import argparse
import os
import math

from SVMclassification import training, getLabel

SIGNS = ["sign is 0",
         "sign is 1",
         "sign is 2",
         "sign is 3",
         "sign is 4",
         "sign is 5",
         "sign is 6",
         "sign is 7",
         "sign is 8",
         "sign is 9",
         "sign is 10",
         "sign is 11",
         "sign is 12",
         "sign is 13",
         "sign is 14",
         "sign is 15",
         "sign is 16",
         "sign is 17",
         "sign is 18",
         "sign is 19",
         "sign is 20",
         "sign is 21",
         "sign is 22",
         "sign is 23"]


if __name__ == "__main__":
    model = training()
    data = cv2.imread("C:\\Users\\young\\Desktop\\just\\2000\\108.png")
    type = getLabel(model, data)
    print(type)
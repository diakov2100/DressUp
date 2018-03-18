import cv2
import numpy as np
import os
from PIL import Image
import face_recognition

def resize_cut(img):
    im = img;
    
    im = Image.open(img)
    nx, ny = im.size
    im2 = im.resize((int(nx * 0.2), int(ny * 0.2)), Image.BICUBIC)
    im2.save("test-lowres.png", dpi=(1,1))


    #remove background
    imgo = cv2.imread("test-lowres.png")
    height, width = imgo.shape[:2]

    #Create a mask holder
    mask = np.zeros(imgo.shape[:2],np.uint8)

    #Grab Cut the object
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    #Hard Coding the Rect… The object must lie within this rect.
    rect = (10,10,width - 0,height - 0)
    cv2.grabCut(imgo,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask = np.where((mask == 2) | (mask == 0),0,1).astype('uint8')
    img1 = imgo * mask[:,:,np.newaxis]

    #Get the background
    background = imgo - img1

    #Change all pixels in the background that are not black to white
    background[np.where((background > [0,0,0]).all(axis = 2))] = [255,255,255]

    #Add the background and the image
    final = background + img1

    return final

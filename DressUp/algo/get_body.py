"""
Description: Extract body of person without head and backdround
"""
import cv2
import numpy as np
import os
from PIL import Image
import face_recognition
from DressUp.algo.resize_cut import resize_cut

def get_body(img):
    image = face_recognition.load_image_file(img)
    face_locations = face_recognition.face_locations(image)
    if (face_locations is None) or (len(face_locations)<1):
        return resize_cut(img)
    image = face_recognition.load_image_file(img)
    face_locations = face_recognition.face_locations(image)

    top, right, bottom, left = face_locations[0]
    pil_image = Image.fromarray(image)
    nx, ny = pil_image.size

    head_size = right - left

    print(head_size, left - 2 * head_size, right + 2 * head_size)

    a = 0
    b = nx

    if left - 2 * head_size > 0:
        a = left - 2 * head_size 
    if right + 2 * head_size < nx:
        b = right + 2 * head_size
    
    face_image = image[bottom:ny, a:b]

    pl_image = Image.fromarray(face_image)
    pl_image.save("withoutface.png", dpi=(1,1))
    im = Image.open("withoutface.png")
    resize_cut(im)   
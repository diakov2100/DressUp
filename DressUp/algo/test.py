""" Test get_outfit """

import os
from PIL import Image
import json
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
import time
import cPickle

#from DressUp.algo.get_outfit import get_outfit
#from DressUp.algo.style_evaluator import load_and_preprocess_image
from get_outfit import get_outfit
from style_evaluator import load_and_preprocess_image

WORKING_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(WORKING_DIR, 'example_images')
DESCRIPTION = os.path.join(IMAGES_DIR, 'desc.json')

PREPROCESSED_FILE = os.path.join(WORKING_DIR, 'preprocessed_clothes_test.pickle')
CENTRAL_ITEM = os.path.join(IMAGES_DIR, 'matching_2.jpg')

class Timer:
    start_time = 0

    @staticmethod
    def start_timer(reason=''):
        Timer.start_time = time.time()
        print('Start timer {}'.format(reason))
    
    @staticmethod
    def stop_timer():
        elapsed_time = time.time() - Timer.start_time
        seconds = int(elapsed_time% 60)
        minutes= int((elapsed_time / 60) % 60)
        print('Finish in {}:{}'.format(minutes, seconds))

def execute():
    with open(PREPROCESSED_FILE, 'rb') as pickleFile:
        clothes = cPickle.load(pickleFile)
    central_item = {
        'features': load_and_preprocess_image(CENTRAL_ITEM),
        'type': 'bottom'
    }
    Timer.start_timer()
    outfit = get_outfit(central_item, clothes)
    Timer.stop_timer()
    print('Outfit:', outfit)
    

if __name__ == "__main__":
    execute()
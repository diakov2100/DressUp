""" Test get_outfit """

import os
from PIL import Image
import json
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
import time

from DressUp.algo.get_outfit import get_outfit
from DressUp.algo.style_evaluator import load_and_preprocess_image
#from get_outfit import get_outfit
#from style_evaluator import load_and_preprocess_image

WORKING_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(WORKING_DIR, 'example_images')
DESCRIPTION = os.path.join(IMAGES_DIR, 'desc.json')

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
    with open(DESCRIPTION) as json_data:
        description = json.load(json_data)
    clothes = []
    Timer.start_timer()
    for item in description:
        img = load_and_preprocess_image(
            os.path.join(IMAGES_DIR, item['filename'])
        )
        clothes.append({
            'image': img,
            'type': item['type']
        })
    Timer.stop_timer()
    Timer.start_timer()
    outfit = get_outfit(clothes[0], clothes[1:])
    Timer.stop_timer()
    print('Central item: {}'.format(description[0]['filename']))
    for item in outfit:
        print(description[item + 1]['filename'])
    

if __name__ == "__main__":
    execute()
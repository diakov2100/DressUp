# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 06:28:02 2018

@author: dyako
"""
import os
from PIL import Image
import json
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
import time
import cPickle

from get_outfit import get_outfit
from style_evaluator import load_and_preprocess_image

from flask import Flask, request

app = Flask(__name__)

import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://admin:989417m@159.65.195.91:27017/dressup')
db = client.dressup

WORKING_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(WORKING_DIR, 'example_images')
DESCRIPTION = os.path.join(IMAGES_DIR, 'desc.json')

PREPROCESSED_FILE = os.path.join(WORKING_DIR, 'preprocessed_clothes_test.pickle')
CENTRAL_ITEM = os.path.join(IMAGES_DIR, 'matching_2.jpg')
 
def search_item(id1):
    
    if db['accessory'].find_one({'id' : id1}) is not None:
        return db['accessory'].find_one({'id' : id1})
    if db['body'].find_one({'id' : id1}) is not None:
        return db['body'].find_one({'id' : id1})
    if db['bottom'].find_one({'id' : id1}) is not None:
        return db['bottom'].find_one({'id' : id1})
    if db['outer'].find_one({'id' : id1}) is not None:
        return db['outer'].find({id : id1})
    if db['shoes'].find_one({'id' : id1}) is not None:
        return db['shoes'].find_one({'id' : id1})
    if db['top'].find_one({'id' : id1}) is not None:
        return db['top'].find_one({'id' : id1})

@app.route("/get_style", methods=['GET', 'POST'])
def get_style():
    type = request.args.get('type')
    img = request.args.get('img')
    collection = db[type]
    '''
    for raw in collection.find():
        if raw.images.uri == img:
            break;
    '''
    with open(PREPROCESSED_FILE, 'rb') as pickleFile:
        clothes = cPickle.load(pickleFile)
    central_item = {
                'features': load_and_preprocess_image(img),
                'type': type
    }
    outfit = get_outfit(central_item, clothes)
    res=[]
    raw=search_item(outfit[0]);
    res.append({'price': raw['price'], 'images': raw['images'], 'name': raw['name'], 'type': raw['type'],  'source':raw['source']})
    raw=search_item(outfit[1]);
    res.append({'price': raw['price'], 'images': raw['images'], 'name': raw['name'], 'type': raw['type'],  'source':raw['source']})
    return json.dump(res)
    
app.run(host='0.0.0.0')

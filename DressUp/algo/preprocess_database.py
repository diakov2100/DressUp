from pymongo import MongoClient
import json
from tqdm import tqdm
import os
import cPickle

from style_evaluator import load_and_preprocess_image_from_url

COLLECTIONS = ['bottom', 'top', 'shoes']

WORKING_DIR = os.path.dirname(__file__)
OUTPUT_FILE = os.path.join(WORKING_DIR, 'preprocessed_clothes.pickle')

def process_collection(db, collection_name):
    collection = db[collection_name]
    cursor = collection.find({}, no_cursor_timeout=True)
    processed = []
    for document in tqdm(cursor):
        id = document['id']
        img_url = document['images'][0]['uri']
        processed.append({
            'id': id,
            'type': collection_name,
            'features': load_and_preprocess_image_from_url(img_url)
        })
    cursor.close()
    return processed

def save_processed(processed):
    with open(OUTPUT_FILE, "wb") as output_file:
        cPickle.dump(processed, output_file)

def execute():
    client = MongoClient('mongodb://admin:989417m@159.65.195.91:27017/dressup')
    db = client.dressup
    processed = []
    for collection_name in COLLECTIONS:
        print('Start processing', collection_name)
        processed.extend(process_collection(db, collection_name))
    save_processed(processed)

if __name__ == "__main__":
    execute()
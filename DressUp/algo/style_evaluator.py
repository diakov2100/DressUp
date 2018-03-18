'''
Application that evaluates the stylistic visual similarity of a pair of user
input images of clothes or jewelry. Uses the learned weights from training the 
siamese network.
'''
from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import numpy as np
#from DressUp.algo.siamese_net import contrastive_loss
from siamese_net import contrastive_loss
from keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg16 import preprocess_input, VGG16
from keras.models import Sequential, load_model
from keras.layers import Input, Flatten
import urllib, cStringIO

#Load trained model and value for rescaling
WORKING_DIR = os.path.dirname(__file__)

model = load_model(os.path.join(WORKING_DIR, 'models', 'best_model.h5'), custom_objects={'contrastive_loss': contrastive_loss})
max_value = np.load(os.path.join(WORKING_DIR, 'data', 'max_value.npy'))

EXAMPLES_DIR = os.path.join(WORKING_DIR, 'example_images')
PATH_1 = os.path.join(EXAMPLES_DIR, 'shirt-1.jpg')
PATH_2 = os.path.join(EXAMPLES_DIR, 'matching_2.jpg')

def load_and_preprocess_image(path_or_image):
    img = load_img(path_or_image, target_size=(224, 224))
    img = preprocess_image(img)
    img = push_through_vgg(img) / max_value
    return img

def load_and_preprocess_image_from_url(url):
    try:
        img = cStringIO.StringIO(urllib.urlopen(url).read())
        img = load_and_preprocess_image(img)
    except:
        print('This is not a valid url or image.')
        print('url:', url)
        sys.exit(1)
    img = cStringIO.StringIO(urllib.urlopen(url).read())
    return load_and_preprocess_image(img)

def preprocess_image(img):
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img
   
def push_through_vgg(img):
    seq = Sequential()
    seq.add(VGG16(weights='imagenet', include_top=False, input_tensor=Input(shape=(3,224,224,))))
    seq.add(Flatten())
    pred_img = seq.predict(img)
    return pred_img

def evaluate_pure(img_1, img_2):
    return model.predict([img_1, img_2])
    
    
def evaluate():
    print('Image 1 of 2:')
    img_1 = load_and_preprocess_image(PATH_1)
    print('Image 2 of 2:')
    img_2 = load_and_preprocess_image(PATH_2)
    print('Calculating the score...')
    return model.predict([img_1, img_2])
    
    
if __name__ == "__main__":
    pred = evaluate()
    print('This outfit gets a score of {:1.2f}.'.format(float(pred)))
    print('Your result:')
    if float(pred)<=.82:
        print('Nice, this looks good together!')
    else:
        print('Sorry, these styles do not match.')

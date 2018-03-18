"""
Routes and views for the flask application.
"""
import os
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from DressUp import app
from werkzeug.utils import secure_filename
from PIL import Image
from DressUp.algo.get_body import get_body
from DressUp.algo.compare_colors import compare
from colorthief import ColorThief
import json
    
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://admin:989417m@159.65.195.91:27017/dressup')
db = client.dressup


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      im = Image.open(f);
      body = get_body(f);
      color_thief = ColorThief(f);
      dominant_color = color_thief.get_color(quality=1);
    # build a color palette
      palette = color_thief.get_palette(color_count=2);
      res=[]
      if (sum(palette[0])> sum(palette[1])) and (sum(palette[0])> sum(palette[2])):
        res=[(palette[2][0], palette[2][1], palette[2][2]),(palette[1][0], palette[1][1], palette[1][2])]
      if (sum(palette[1])> sum(palette[0])) and (sum(palette[1])> sum(palette[2])):
        res=[(palette[2][0], palette[2][1], palette[2][2]),(palette[0][0], palette[0][1], palette[0][2])]
      
      res=[(palette[0][0], palette[0][1], palette[0][2]),(palette[1][0], palette[1][1], palette[1][2])]
      return json.dumps(res);

@app.route('/items', methods = ['GET'])
def get_items():
    type=request.args.get('type')
    set1=json.loads(request.args.get('set1'))
    set2=json.loads(request.args.get('set2'))
    set3=json.loads(request.args.get('set3'))
    collection = db[type]
    res=[]
    for raw in collection.find():
        if compare(set1, set2, set3, raw['colors']):
            res.append({'price': raw['price'], 'images': raw['images'], 'name': raw['name'], 'type': raw['type'],  'source':raw['source']})
        if len(res) == 4:
            break
    print("Request result ", json.dumps(res))
    return json.dumps(res);
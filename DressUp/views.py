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
from colorthief import ColorThief
import json

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
      body = get_body(im);
      color_thief = ColorThief(f);
      dominant_color = color_thief.get_color(quality=1);
    # build a color palette
      palette = color_thief.get_palette(color_count=3);
      return json.dumps(palette);

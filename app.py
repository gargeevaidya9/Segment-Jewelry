# coding=utf-8
import sys
import os
import glob
import re
import cv2
import numpy as np
from keras.models import load_model
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# Define a flask app
app = Flask(__name__, template_folder='.')

# Loading trained model
MODEL_PATH = 'model_rgba_a_onlyscrapped_and_newdata.h5'
model = load_model(MODEL_PATH)
print('Model loaded. Check http://127.0.0.1:5000/')

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('base.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', f.filename)
        f.save(file_path)

        ext = (str(f.filename).split('.'))[1]
        name = (str(f.filename).split('.'))[0]

        if ext == '.png':
            img = cv2.imread(file_path)
        else:
            i = cv2.imread(file_path)
            cv2.imwrite( basepath + '/uploads/' + name + '.png', i)
            img = cv2.imread(basepath + '/uploads/' + name + '.png')
            f.filename = str(name + '.png')
          
    
        img = cv2.resize(img,(256,256))
        img_BGRA = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img_norm = (img_BGRA - np.mean(img_BGRA))/np.max(img_BGRA)
        X = np.expand_dims(img_norm, axis=0)
        preds = np.argmax(model.predict(X),axis=-1)
        new_A = np.asarray(preds.reshape(256,256),dtype='uint8')
        R,G,B,A = cv2.split(img_BGRA)
        final = cv2.merge((R,G,B,new_A))
        final_resized = cv2.resize(final,(256,256))
        cv2.imwrite('static/js/Results/bg-removed-' + f.filename, final_resized)
        a=f.filename

    return a
        
    return None


if __name__ == '__main__':
    app.run(debug=True)

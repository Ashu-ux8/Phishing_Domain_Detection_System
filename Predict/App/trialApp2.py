from flask import Flask, request, render_template
import numpy as np
import joblib
from urllib.parse import urlparse
import socket
import time,requests
import dns.resolver
import textwrap
import Check as chP
import pickle

app = Flask(__name__)

# Load the trained model
model = joblib.load('C:/Users/jiter/Downloads/Predict1/Predict/FinalPred.pkl')

#print(model)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])

def predict():
    # Get URL input from the user
    url = request.form['url']
    
    vals = chP.extract_featuresS(url)
    x = [vals[key] for key in vals.keys()]
    model_input = (np.array(x, dtype=object)).reshape(1, -1)
    print(x)

    # Make prediction using the model
    pred = model.predict(model_input)

    
    # Return prediction result to the user
    return render_template('result.html', prediction=pred)

# def predict():
#     # Get URL input from the user
#     url = request.form['url']
    
#     # Extract features from the URL
#     features = chP.extract_featuresS(url)
#     # x = [vals[key] for key in vals.keys()]
#     # model_input = (np.array(x, dtype=object)).reshape(1, -1)
#     # print(x)

#     # Make prediction using the model
#     pred = model.predict([list(features.values())])
    
    # Return prediction result to the user

    # return render_template('result.html', prediction=0)

if __name__ == '__main__':
    app.run(debug=True)

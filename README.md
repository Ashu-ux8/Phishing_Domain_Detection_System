
# Phishing Website Detection System

This project is a web-based application built using Flask, designed to predict whether a given URL is legitimate or a phishing attempt. It uses machine learning, specifically the XGBoost classifier, to analyze features extracted from the URL and return a prediction.


## Features

 - URL Analysis: Extracts features from a user-inputted URL for phishing detection.
 - XGBoost Model: A trained XGBoost model is used for the predictions, stored as a .pkl file.
 - Web Interface: A simple, user-friendly web interface where users can input URLs, built with HTML and CSS.
 - Results Display: The prediction result (whether the URL is legitimate or phishing) is shown to the user in real-time.


## File Description


|-- PREDICT/

    |-- __pycache__/
    |-- App/
        |-- trialApp.py           # Trial script for testing app components
        |-- trialApp2.py          # Another trial script for further tests
    |-- dataset/
        |-- datasetNew.csv        # Dataset used for training the model
    |-- Predictors/
        |-- FinalPred.pkl         # Final XGBoost model for prediction
    |-- static/
        |-- css/                  # Styling files
        |-- fonts/
        |-- images/
        |-- js/                   # JavaScript files
    |-- templates/
        |-- about.html            # 'About' page template
        |-- index.html            # Main page for user input
        |-- result.html           # Displays the prediction result
        |-- service.html          # Services page template
        |-- team.html             # Team page template
        |-- why.html              # Explanation page template
    |-- app3.py                   # Main Flask application file
    |-- Check.py                  # Additional script for checking functionality
    |-- output.png                # Screenshot of project output

## Key Components

    1. Flask App (app3.py)
The main Flask application file that handles routing and user interactions. Users can input a URL, and the app will use the model stored in Predictors/FinalPred.pkl to make predictions.

    2. XGBoost Model
The machine learning model (FinalPred.pkl) has been trained using features extracted from URLs. This model is responsible for classifying URLs as either phishing or legitimate.

    3. Templates
HTML templates are stored in the templates/ folder, with separate pages for input, results, and additional info about the project.

    4. Static Files
The static assets (CSS, images, JavaScript) are located in the static/ folder, helping to design and style the front end.

    5. Dataset
The dataset (dataset/datasetNew.csv) contains the features used to train the XGBoost model. Features include aspects of the URL, such as its length, the presence of suspicious characters, etc.
## Installation

To install and run this project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/phishing-url-detector.git

2. Navigate to the project directory
    ```bash
   cd phishing-url-detector

3. Installation of required dependancies
    ```bash
    pip install -r requirements.txt
4. Run the flask application: 
    ```bash
    python app3.py

5. Access the app in your browser:
    ```bash
    http://127.0.0.1:5000

    
## Usage/Examples
 - Navigate to the main page.
 - Enter a URL in the provided input field.
 - Click on 'Check URL' to get the prediction result.
 - The model will classify the URL as either "Legitimate" or "Phishing."
## Model Details
 - Algorithm: XGBoost Classifier
 - Model File: The pre-trained model is stored in Predictors/FinalPred.pkl.
 - Training Data: A custom dataset of URLs, including legitimate and phishing examples, is used to train the model.

## Contributing

Contributions are always welcome!

If you find any bugs or want to add new features, feel free to fork the repository and create a pull request.
## License

[MIT](https://choosealicense.com/licenses/mit/)

This project is licensed under the MIT License - see the LICENSE file for details.

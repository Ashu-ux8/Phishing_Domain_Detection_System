from urllib.parse import urlparse, parse_qs
from datetime import datetime
import socket
import whois
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
from xgboost import XGBClassifier
import Check as pCheck
import requests
import time
import tldextract
from ipwhois import IPWhois
import dns.resolver
import ipwhois
from ipwhois import IPWhois
import certifi
import ssl
import xgboost as xgb
import pickle
from flask import Flask, request, render_template

app = Flask(__name__)
# Function to extract features from a URL

model = joblib.load('Predict/FinalPredictor.pkl')

def extract_features(url):
    # Parse the URL
    dom = urlparse(url).hostname
    parsed_url = urlparse(url)
    print("Port: ",parsed_url.port)
    print("netloc: ",parsed_url.netloc)
    print("Path: ",parsed_url.path)
    print("Query: ", parsed_url.query)
    print("Hostname: ", parsed_url.hostname)
    # Extract domain components using tldextract
    domain_extract = tldextract.extract(url)

    # Initialize features dictionary
    features = {}

    # Feature 1: Directory Length
    features['directory_length'] = len(parsed_url.path)

    # Feature 2: Quantity of slashes in the URL
    features['qty_slash_url'] = parsed_url.path.count('/')

    # Feature 3: Quantity of plus symbols in parameters
    features['qty_plus_params'] = url.count('+')

    # Feature 4: Quantity of dots in the domain
    features['qty_dot_domain'] = parsed_url.netloc.count('.')

    # Feature 5: Time domain activation (not extracted from URL, fill with a default value)
    features['time_domain_activation'] = pCheck.calculate_time_activation(parsed_url.netloc)

    # Feature 6: Quantity of dots in parameters
    params = parse_qs(parsed_url.query)
    qty_dot_params = sum(param.count('.') for param in params)
    features['qty_dot_params'] = qty_dot_params

    # Feature 7: Quantity of hyphens in the directory
    features['qty_hyphen_directory'] = parsed_url.path.count('-')

    # Feature 8: Domain in IP format (not extracted from URL, fill with a default value)
    features['domain_in_ip'] = 1 if parsed_url.netloc.replace('.', '').isdigit() else 0

    # Feature 9: URL shortened (not extracted from URL, fill with a default value)
    features['url_shortened'] =  1 if len(parsed_url.netloc) < 15 else 0

    # Feature 10: Quantity of TLDs in the URL
    features['qty_tld_url'] = len(domain_extract.suffix)

    # Feature 11: Quantity of percent symbols in the file
    features['qty_percent_file'] = parsed_url.path.count('%')

    # Feature 12: Quantity of equal symbols in the URL
    features['qty_equal_url'] = url.count('=')

    # Feature 13: Quantity of underline symbols in parameters
    features['qty_underline_params'] = url.count('_')

    # Feature 14: Quantity of underline symbols in the file
    features['qty_underline_file'] = parsed_url.path.count('_')

    # Feature 15: Length of the URL
    features['length_url'] = len(url)

    # Feature 16: Quantity of @ symbols in the URL
    features['qty_at_url'] = url.count('@')

    # Feature 17: Quantity of plus symbols in the URL
    features['qty_plus_url'] = url.count('+')

    # Feature 18: Quantity of resolved IPs in the URL (not extracted from URL, fill with a default value)
    features['qty_ip_resolved'] = pCheck.count_ip_resolved(parsed_url)

    # Feature 19: Quantity of comma symbols in the directory
    features['qty_comma_directory'] = parsed_url.path.count(',')

    # Feature 20: Quantity of name servers (not extracted from URL, fill with a default value)
    features['qty_nameservers'] = pCheck.count_nameservers(url)

    # Feature 21: Quantity of dots in the URL
    features['qty_dot_url'] = url.count('.')

    # Feature 22: Quantity of equal symbols in the directory
    features['qty_equal_directory'] = parsed_url.path.count('=')

    # Feature 23: Quantity of hyphens in the domain
    features['qty_hyphen_domain'] = domain_extract.domain.count('-')

    # Feature 24: ASN IP (not extracted from URL, fill with a default value)
    features['asn_ip'] = pCheck.get_asn(url)

    # Feature 25: TLS/SSL certificate (not extracted from URL, fill with a default value)
    features['tls_ssl_certificate'] = pCheck.extract_certificate(url)

    # Feature 26: Quantity of hyphens in the URL
    features['qty_hyphen_url'] = url.count('-')

    # Feature 27: Quantity of comma symbols in the file
    features['qty_comma_file'] = parsed_url.path.count(',')

    # Feature 28: TTL hostname (not extracted from URL, fill with a default value)
    features['ttl_hostname'] = pCheck.get_ttl(url)

    # Feature 29: Length of parameters
    params_length = sum(len(param) for param in params)
    features['params_length'] = params_length

    # Feature 30: Domain SPF (not extracted from URL, fill with a default value)
    features['domain_spf'] = pCheck.extract_spf(url)

    # Feature 31: Quantity of MX servers (not extracted from URL, fill with a default value)
    features['qty_mx_servers'] = pCheck.get_number_of_mx_servers(dom)

    # Feature 32: Quantity of parameters
    features['qty_params'] = len(params)

    # Feature 33: Quantity of "&"
    features['qty_and_params'] = url.count('&')
    
    # Feature 1: qty_redirects (not possible to extract from URL directly)
    # You may need to use a library or technique to follow redirects and count them
    features['qty_redirects']= pCheck.count_redirects(url)
    
    # Feature 2: time_response (not possible to extract from URL directly)
    # You can use the requests library to get the response time
    try:
        response = requests.head(url)
        features['time_response'] = response.elapsed.total_seconds()
    except requests.exceptions.RequestException:
        features['time_response'] = -1
    
    # Feature 3: qty_underline_url
    features['qty_underline_url'] = url.count('_')
    
    # Feature 4: qty_slash_directory
    features['qty_slash_directory'] = parsed_url.path.count('/')
    
    # Feature 5: qty_percent_directory
    features['qty_percent_directory'] = parsed_url.path.count('%')
    
    # Feature 6: file_length
    features['file_length'] = len(parsed_url.path.split('/')[-1])
    
    # Feature 7: qty_comma_url
    features['qty_comma_url'] = url.count(',')
    
    # Feature 8: qty_hyphen_file
    features['qty_hyphen_file'] = parsed_url.path.count('-')
    
    # Feature 9: qty_percent_url
    features['qty_percent_url'] = url.count('%')
    
    # Feature 10: time_domain_expiration (not possible to extract from URL directly)
    # You may need to use a WHOIS lookup to get domain expiration information
    try:
        domain = tldextract.extract(parsed_url.netloc)
        whois_info = whois.whois(domain.registered_domain)
        features['time_domain_expiration'] = (whois_info.expiration_date - whois_info.creation_date).days if whois_info.expiration_date is not None else None
    except Exception:
        features['time_domain_expiration'] = -1
    
    # Feature 11: qty_dot_directory
    features['qty_dot_directory'] = parsed_url.path.count('.')
    
    # Feature 12: qty_tilde_url
    features['qty_tilde_url'] = url.count('~')
    
    # Feature 13: domain_length
    features['domain_length'] = len(parsed_url.netloc)
    
    # Feature 14: qty_underline_directory
    features['qty_underline_directory'] = parsed_url.path.count('_')
    
    # Feature 15: qty_vowels_domain
    vowels = 'aeiouAEIOU'
    features['qty_vowels_domain'] = sum(parsed_url.netloc.count(vowel) for vowel in vowels)
    
    # Feature 16: qty_dot_file
    features['qty_dot_file'] = parsed_url.path.count('.')
    
    # Feature 17: qty_equal_params
    features['qty_equal_params'] = url.count('=')
    
    return features
    


# Example usage

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get URL input from the user
    url = request.form['url']
    
    # Extract features from the URL
    vals = extract_features(url)
    x = [vals[key] for key in vals.keys()]
    model_input = (np.array(x, dtype=object)).reshape(1, -1)
    print(x)

    # Make prediction using the model
    pred = model.predict(model_input)
    
    # Return prediction result to the user
    return render_template('result.html', prediction=0)


if __name__ == '__main__':
    app.run(debug=True)


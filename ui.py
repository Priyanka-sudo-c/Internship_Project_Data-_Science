from flask import Flask, request, render_template
import pandas as pd
import shap
import joblib
import numpy as np
import matplotlib.pyplot as plt
import os

# Initialize Flask app
app = Flask(__name__)mm

# Load the trained phishing model
MODEL_PATH = "phishing_model.pkl"
model = joblib.load(MODEL_PATH)

# Ensure SHAP visualizations can be displayed
shap.initjs()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    df = pd.read_csv(file)
    
    # Make predictions
    predictions = model.predict(df)
    df['Prediction'] = predictions
    
    # SHAP Explanation
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df)
    
    # Save SHAP plot
    shap.summary_plot(shap_values, df, show=False)
    plt.savefig("static/shap_summary.png")
    plt.close()
    
    return render_template('result.html', tables=[df.to_html()], shap_img="static/shap_summary.png")

if __name__ == '__main__':
    app.run(debug=True)

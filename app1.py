from flask import Flask, request, jsonify
import joblib
import pandas as pd
import shap

# Load trained model
model = joblib.load("phishing_model.pkl")

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Phishing Detection API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame(data)
        prediction = model.predict(df)
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/explain', methods=['POST'])
def explain():
    try:
        data = request.get_json()
        df = pd.DataFrame(data)
        
        # SHAP explanation
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(df)
        
        return jsonify({"shap_values": shap_values[1].tolist()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

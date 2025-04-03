import pandas as pd
import numpy as np
import shap
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


import sys
sys.path.append("<path_to_shap>")
import shap

# Load dataset
df = pd.read_csv("dataset_phishing.csv")

# Preprocess Data (Assuming last column is the target variable)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "phishing_model.pkl")

# Model Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# SHAP Analysis
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Plot SHAP Summary
shap.summary_plot(shap_values[1], X_test)

# Save SHAP plot
plt.savefig("shap_summary.png")
print("SHAP analysis completed and saved as shap_summary.png")

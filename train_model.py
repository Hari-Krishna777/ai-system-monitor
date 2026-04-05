import pandas as pd
from sklearn.ensemble import IsolationForest

# load data
data = pd.read_csv("data.csv")

print(data.columns)  # debug (optional)

data = data[['cpu', 'ram', 'disk']]

# train model
model = IsolationForest(contamination=0.05)
model.fit(data)

# save model
import joblib
joblib.dump(model, "model.pkl")

print("Model trained and saved!")

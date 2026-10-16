import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Loading dataset.csv...")
# 1. Load your newly generated CSV data
df = pd.read_csv('dataset.csv')

# 2. Separate features (X) from the target label (y)
X = df[['lines_added', 'lines_deleted', 'code_complexity']]
y = df['is_bug_prone']

# 3. Split the dataset into a Training set and a Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training the Bug Propensity Predictor model (Random Forest)...")
# 4. Initialize and fit the Machine Learning classifier
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate the model performance
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Training Complete! Baseline Test Accuracy: {accuracy * 100:.2f}%")

# 6. Save the trained model binary to disk so our Git hook can load it instantly later
model_filename = 'bug_predictor.pkl'
joblib.dump(model, model_filename)
print(f"Saved trained model asset to: {model_filename}")

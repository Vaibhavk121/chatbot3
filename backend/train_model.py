# backend/train_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC # Linear Support Vector Classifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from data import training_data # Import your training data

print("Starting model training...")

# Convert training data to a pandas DataFrame for easier handling
df = pd.DataFrame(training_data)

# Ensure there's data for every intent for robust splitting, especially with small datasets.
# This is a basic check; more sophisticated checks might be needed for highly imbalanced data.
if df['intent'].nunique() < 2:
    print("Error: Need at least two unique intents to train the model.")
    exit()

# Stratify by intent if possible to ensure representative splits, especially if some intents have few samples
# test_size could be adjusted based on dataset size
try:
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['intent'], test_size=0.2, random_state=42, stratify=df['intent']
    )
except ValueError: # Happens if an intent has only 1 sample with stratify
    print("Warning: Could not stratify split, proceeding without it. Ensure all intents have at least 2 samples.")
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['intent'], test_size=0.2, random_state=42
    )


# Create a pipeline: TfidfVectorizer for text features and LinearSVC for classification
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1,2))), # Added stop_words and ngram_range
    ('classifier', LinearSVC(random_state=42, C=1.0, class_weight='balanced')) # Added C and class_weight
])

# Train the model
model_pipeline.fit(X_train, y_train)

print("Model training complete.")

# Evaluate the model
y_pred = model_pipeline.predict(X_test)
print("\nClassification Report:")
# Added zero_division parameter for intents that might not be in the test set after split
print(classification_report(y_test, y_pred, zero_division=0))

# Save the trained model
model_filename = 'intent_model.joblib'
joblib.dump(model_pipeline, model_filename)
print(f"\nModel saved as {model_filename}")

# Example test (optional)
# new_queries = ["what skills for software engineer", "how much does a doctor make", "i like sports", "thanks a lot"]
# predicted_intents = model_pipeline.predict(new_queries)
# for query, intent in zip(new_queries, predicted_intents):
# print(f"Query: '{query}' -> Predicted Intent: '{intent}'")
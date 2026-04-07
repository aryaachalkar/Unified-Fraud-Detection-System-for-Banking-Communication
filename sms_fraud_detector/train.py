import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from preprocess import preprocess

# 1. Load dataset
print("Loading dataset...")
df = pd.read_csv("SMSSpamCollection", sep="\t",
                 names=["label", "message"], encoding="latin-1")
df["label_num"] = df["label"].map({"ham": 0, "spam": 1})
print(f"Dataset loaded: {len(df)} messages")
print(df["label"].value_counts())

# 2. Preprocess
print("\nPreprocessing messages...")
df["clean"] = df["message"].apply(preprocess)

# 3. Split
X_train, X_test, y_train, y_test = train_test_split(
    df["clean"], df["label_num"],
    test_size=0.2, random_state=42, stratify=df["label_num"]
)

# 4. Vectorize
print("Vectorizing text with TF-IDF...")
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    stop_words="english",
    sublinear_tf=True
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)

# 5. Train
print("Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, C=5)
model.fit(X_train_vec, y_train)

# 6. Evaluate
preds = model.predict(X_test_vec)
print("\n--- Model Evaluation ---")
print(classification_report(y_test, preds, target_names=["ham", "spam"]))

# 7. Save
joblib.dump(model,      "sms_fraud_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("Model saved: sms_fraud_model.pkl")
print("Vectorizer saved: tfidf_vectorizer.pkl")
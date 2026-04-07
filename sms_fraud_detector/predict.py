import joblib
import re
from preprocess import preprocess

# Load saved model and vectorizer
model      = joblib.load("sms_fraud_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def predict_sms(message: str) -> dict:
    cleaned   = preprocess(message)
    vec       = vectorizer.transform([cleaned])
    pred      = model.predict(vec)[0]
    proba     = model.predict_proba(vec)[0]

    label      = "SPAM / FRAUD" if pred == 1 else "LEGITIMATE"
    confidence = round(max(proba) * 100, 1)

    signals = []
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["otp", "pin", "password"]):
        signals.append("requests OTP/PIN/password")
    if any(w in msg_lower for w in ["urgent", "immediately", "expire", "blocked", "suspended"]):
        signals.append("urgency language detected")
    if re.search(r"http\S+|bit\.ly|tinyurl", msg_lower):
        signals.append("contains a URL")
    if re.search(r"\b(won|winner|prize|lottery|reward|congratulations)\b", msg_lower):
        signals.append("prize/lottery language")
    if re.search(r"\b\d{10}\b", msg_lower):
        signals.append("contains a phone number")

    return {
        "verdict":    label,
        "confidence": f"{confidence}%",
        "signals":    signals if signals else ["no strong indicators"]
    }

if __name__ == "__main__":
    print("=" * 55)
    print("       SMS Fraud Detector — type a message below")
    print("=" * 55)
    print("(type 'quit' to exit)\n")

    while True:
        msg = input("Paste SMS: ").strip()
        if msg.lower() == "quit":
            print("Exiting.")
            break
        if not msg:
            continue

        result = predict_sms(msg)
        print(f"\n  Verdict    : {result['verdict']}")
        print(f"  Confidence : {result['confidence']}")
        print(f"  Signals    : {', '.join(result['signals'])}")
        print("-" * 55 + "\n")
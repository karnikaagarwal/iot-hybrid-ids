import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

print("📥 Loading dataset...")

data = pd.read_csv("dataset.csv")

features = [
    "packet_count",
    "rate",
    "unique_ports",
    "avg_packet_size",
    "tcp_flag_sum"
]

X = data[features]
y = data["label"]

print("🧹 Splitting...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("🌲 Training...")
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

print("📊 Accuracy:", model.score(X_test, y_test))

joblib.dump(model, "model.pkl")

print("✅ MODEL READY")

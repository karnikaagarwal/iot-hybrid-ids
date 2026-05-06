from sklearn.preprocessing import LabelEncoder, StandardScaler

categorical_cols = ["proto", "service", "state"]


def fit_preprocess(df):
    df = df.copy()

    df = df.drop(columns=["id"], errors="ignore")

    # Encode categorical features
    encoders = {}
    for col in categorical_cols:
        if col in df:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le

    # Encode attack labels
    attack_encoder = LabelEncoder()
    df["attack_cat"] = attack_encoder.fit_transform(df["attack_cat"])

    X = df.drop(columns=["attack_cat"])
    y = df["attack_cat"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, encoders, attack_encoder


def transform(df, scaler, encoders):
    df = df.copy()

    df = df.drop(columns=["id"], errors="ignore")

    for col in categorical_cols:
        if col in df:
            le = encoders[col]
            df[col] = df[col].apply(
                lambda x: le.transform([str(x)])[0] if str(x) in le.classes_ else 0
            )

    return scaler.transform(df)

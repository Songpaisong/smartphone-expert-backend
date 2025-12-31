from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# =========================
# LOAD DATASET
# =========================
try:
    df = pd.read_csv("mobile_recommendation_system_dataset.csv")
except Exception as e:
    print("Error load dataset:", e)
    df = pd.DataFrame()

# Bersihkan data
df = df.fillna("")

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "Backend Sistem Pakar Rekomendasi Smartphone Aktif (Railway)"

# =========================
# SISTEM PAKAR (FORWARD CHAINING)
# =========================
@app.route("/recommend", methods=["GET"])
def recommend():
    phone_type = request.args.get("type", "").lower()
    budget = request.args.get("budget", type=int)

    if phone_type == "" or budget is None:
        return jsonify({
            "error": "Parameter 'type' dan 'budget' wajib diisi"
        })

    # RULE BASE (Forward Chaining)
    result = df[
        (df["category"].str.lower() == phone_type) &
        (df["price"] <= budget)
    ]

    # Urutkan hasil terbaik
    result = result.sort_values(
        by=["rating", "price"],
        ascending=[False, True]
    )

    result = result.head(10)

    # Output JSON aman
    output = []
    for _, row in result.iterrows():
        output.append({
            "name": str(row["name"]),
            "price": int(row["price"]),
            "rating": float(row["rating"]),
            "image": str(row["image"]),
            "chipset": str(row.get("chipset", "")),
            "category": str(row.get("category", ""))
        })

    return jsonify(output)

# =========================
# RUN APP (WAJIB RAILWAY)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

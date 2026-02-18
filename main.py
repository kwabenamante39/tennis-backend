from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load datasets
atp_data = pd.read_csv("atp_matches_2023.csv")
wta_data = pd.read_csv("wta_matches_2023.csv")

@app.get("/")
def home():
    return {"message": "Advanced Tennis Prediction Backend Running"}

@app.get("/predict")
def predict(tour: str, player1: str, player2: str):

    if tour.lower() == "atp":
        data = atp_data
    else:
        data = wta_data

    # Recent form (last 10 matches)
    p1_matches = data[(data["winner_name"] == player1) | (data["loser_name"] == player1)].tail(10)
    p2_matches = data[(data["winner_name"] == player2) | (data["loser_name"] == player2)].tail(10)

    p1_wins = len(p1_matches[p1_matches["winner_name"] == player1])
    p2_wins = len(p2_matches[p2_matches["winner_name"] == player2])

    # Head-to-head
    h2h = data[
        ((data["winner_name"] == player1) & (data["loser_name"] == player2)) |
        ((data["winner_name"] == player2) & (data["loser_name"] == player1))
    ]

    p1_h2h = len(h2h[h2h["winner_name"] == player1])
    p2_h2h = len(h2h[h2h["winner_name"] == player2])

    # Weighted scoring
    p1_score = (p1_wins * 2) + (p1_h2h * 3)
    p2_score = (p2_wins * 2) + (p2_h2h * 3)

    total = p1_score + p2_score

    if total == 0:
        return {"error": "Not enough data"}

    p1_prob = (p1_score / total) * 100
    p2_prob = (p2_score / total) * 100

    winner = player1 if p1_prob > p2_prob else player2

    return {
        "player1_probability": round(p1_prob, 2),
        "player2_probability": round(p2_prob, 2),
        "predicted_winner": winner
    }

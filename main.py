from fastapi import FastAPI
import requests
import pandas as pd
from io import StringIO

app = FastAPI()

DATA_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2023.csv"

@app.get("/")
def home():
    return {"message": "Tennis Backend Running"}

@app.get("/predict")
def predict(player1_rank: int, player2_rank: int):

    score1 = 100 - player1_rank
    score2 = 100 - player2_rank

    total = score1 + score2

    prob1 = (score1 / total) * 100
    prob2 = (score2 / total) * 100

    winner = "Player 1" if prob1 > prob2 else "Player 2"

    return {
        "player1_probability": round(prob1, 2),
        "player2_probability": round(prob2, 2),
        "predicted_winner": winner
    }

@app.get("/top_players")
def top_players():
    try:
        response = requests.get(DATA_URL)
        df = pd.read_csv(StringIO(response.text))

        top = df[['winner_name','winner_rank']].dropna().sort_values('winner_rank').head(10)

        return top.to_dict(orient="records")

    except:
        return {"error": "Data fetch failed"}

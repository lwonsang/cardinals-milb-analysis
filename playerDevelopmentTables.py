import csv
import pandas as pd
from collections import defaultdict
from teamStats import get_cardinals_minor_league_stats

MIN_PA = 50
TEAM_ID = 138

def createPlayerDevelopmentTable(df):
    players = {}
    for player_id, group in df.groupby("player_id"):
        players[player_id] = {
            "name": group["player_name"].iloc[0],
            "levels": group.to_dict("records")
        }
        print(players[player_id])

    return players

def createDataTables():
    df = get_cardinals_minor_league_stats(TEAM_ID)
    df["pa"] = df["plate_appearances"]
    df["k_rate"] = df["strikeouts"] / df["plate_appearances"]
    df["bb_rate"] = df["walks"] / df["plate_appearances"]

    df["iso"] = df["slg"].astype(float) - df["avg"].astype(float)

    df["sample_size"] = df["plate_appearances"].apply(classify_sample_size)
    print(df.shape)
    print(df["level"].value_counts())
    print(df.head())

    
    df.to_csv("cardinals.csv", index=False)
    return df

def createPlayerSummary(df):
    player_summary = (
        df
        .groupby(["player_id", "player_name"])
        .agg(
            levels=("level", list),
            total_pa=("plate_appearances", "sum"),
            num_levels=("level", "nunique"),
        )
    )
    print(player_summary.head())
    print(player_summary.shape)
    return player_summary

def createQualifiedRankings(df):
    qualified_df = df[df["pa"] >= MIN_PA]
    cards_df = qualified_df[
        [
            "player_name",
            "level",
            "age",
            "plate_appearances",
            "sample_size",
            "home_runs",
            "avg",
            "obp",
            "slg",
            "ops",
            "k_rate",
            "bb_rate",
            "iso"
        ]
    ].sort_values("ops", ascending=False).head(15)
    cards_df.to_csv("top_cards.csv", index=False)
    return cards_df

def classify_sample_size(pa):
    if pa < 25:
        return "Very small"
    elif pa < 50:
        return "Small"
    elif pa < 100:
        return "Moderate"
    else:
        return "Large"


if __name__ == "__main__":
    df = createDataTables()
    createPlayerSummary(df)
    createQualifiedRankings(df)
    createPlayerDevelopmentTable(df)
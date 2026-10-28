import pandas as pd
import streamlit as st
from processing.config import LEVEL_ORDER

pitching = pd.read_parquet(
    "data/processed/historical_pitching.parquet"
)

pitching_development = pd.read_parquet(
    "data/processed/pitching_development.parquet"
)

def get_all_pitching_data():
    pitching["level"] = pd.Categorical(
        pitching["level"],
        categories = LEVEL_ORDER,
        ordered = True
    )
    return pitching.sort_values(["season", "level"])

def get_seasonal_pitching_data():
    return sorted(
        pitching["season"].dropna().unique(),
        reverse=True,
    )

def get_level_pitching_data():
    pitching["level"] = pd.Categorical(
        pitching["level"],
        categories = LEVEL_ORDER,
        ordered = True
    )

    return list(
        pitching["level"].dropna().unique(),
    )

def get_pitching_development_data():
    pitching_development["level"] = pd.Categorical(
        pitching_development["level"],
        categories = LEVEL_ORDER,
        ordered = True
    )
    return pitching_development.sort_values(["season", "level"])

def get_top_pitchers(pitching_season, pitching_level, min_ip):
    development_columns = [
        "player_id",
        "season",
        "level",
        "era_vs_level",
        "era_vs_age_level",
    ]

    available_columns = [
        col for col in development_columns
        if col in pitching_development.columns
    ]

    pitcher_board = pitching.merge(
        pitching_development[available_columns].drop_duplicates(
            subset=["player_id", "season", "level"]
        ),
        on=["player_id", "season", "level"],
        how="left",
    )

    pitcher_board = pitcher_board[
        pitcher_board["season"] == pitching_season
    ].copy()

    if pitching_level != "All":
        pitcher_board = pitcher_board[
            pitcher_board["level"] == pitching_level
        ]

    pitcher_board = pitcher_board[
        pitcher_board["ip_decimal"] >= min_ip
    ].copy()

    pitcher_board = pitcher_board.sort_values(
        "era_vs_level",
        ascending=True,
        na_position="last",
    )

    return pitcher_board

def get_basic_pitching_column_config():
    column_config={
        "player_id": None,
        "player_name": "Player Name",
        "team_id": None,
        "team_name": "Team Name",
        "season": "Season",
        "league": None,
        "level": "Level",
        "position": None,
        "age": "Age",
        "games": None,
        "games_started": None,
        "wins": None,
        "losses": None,
        "innings_pitched": "IP",
        "hits_allowed": None,
        "runs_allowed": None,
        "earned_runs": None,
        "home_runs_allowed": None,
        "walks": None,
        "strikeouts": None,
        "era": st.column_config.NumberColumn( "ERA", format="%.2f", ),
        "whip": st.column_config.NumberColumn( "WHIP", format="%.2f", ),
        "strikeouts_per_9": st.column_config.NumberColumn( "K/9", format="%.2f", ),
        "walks_per_9": st.column_config.NumberColumn( "BB/9", format="%.2f", ),
        "hits_per_9": st.column_config.NumberColumn( "H/9", format="%.2f", ),
        "strikeout_walk_ratio": st.column_config.NumberColumn( "K/BB", format="%.2f", ),
        "saves": None,
        "holds": None,
        "ip_decimal": None,
        "hr_per_9": st.column_config.NumberColumn( "HR/9", format="%.2f", ),
    }

    return column_config

def get_top_pitchers_column_config():
    column_config={
        "player_id": None,
        "player_name": "Player",
        "age": "Age",
        "level": "Level",
        "ip": "IP",
        "era": st.column_config.NumberColumn( "ERA", format="%.2f", ),
        "era_vs_level": st.column_config.NumberColumn( "ERA vs Level", format="%.2f", ),
        "era_vs_age_level": st.column_config.NumberColumn( "ERA vs Age Level", format="%.2f", ),
    }

    return column_config

def get_pitcher_baseline_comparison_column_config():
    column_config={
        "player_id": None,
        "player_name": None,
        "team_id": None,
        "team_name": None,
        "season": "Season",
        "league": None,
        "level": "Level",
        "position": None,
        "age": "Age",
        "games": None,
        "games_started": None,
        "wins": None,
        "losses": None,
        "innings_pitched": "IP",
        "hits_allowed": None,
        "runs_allowed": None,
        "earned_runs": None,
        "home_runs_allowed": None,
        "walks": None,
        "strikeouts": None,
        "era": st.column_config.NumberColumn( "ERA", format="%.2f", ),
        "whip": None,
        "strikeouts_per_9": None,
        "walks_per_9": None,
        "hits_per_9": None,
        "hr_per_9": None,
        "strikeout_walk_ratio": st.column_config.NumberColumn( "K/BB", format="%.2f", ),
        "saves": None,
        "holds": None,
        "ip_decimal": None,
        "level_players": None,
        "level_innings_pitched": None,
        "level_era": st.column_config.NumberColumn( "Level ERA", format="%.2f", ),
        "level_whip": None,
        "level_strikeouts_per_9": None,
        "level_walks_per_9": None,
        "level_hits_per_9": None,
        "level_hr_per_9": None,
        "level_strikeout_walk_ratio": st.column_config.NumberColumn( "Level K/BB", format="%.2f", ),
        "age_level_players": None,
        "age_level_innings_pitched": None,
        "age_level_era": st.column_config.NumberColumn( "Age Level ERA", format="%.2f", ),
        "age_level_whip": None,
        "age_level_strikeouts_per_9": None,
        "age_level_walks_per_9": None,
        "age_level_hits_per_9": None,
        "age_level_hr_per_9": None,
        "age_level_strikeout_walk_ratio": st.column_config.NumberColumn( "Age Level K/BB", format="%.2f", ),
        "era_vs_level": st.column_config.NumberColumn( "ERA vs Level", format="%.2f", ),
        "whip_vs_level": None,
        "strikeouts_per_9_vs_level": None,
        "hits_per_9_vs_level": None,
        "walks_per_9_vs_level": None,
        "hr_per_9_vs_level": None,
        "strikeout_walk_ratio_vs_level": None,
        "era_vs_age_level": None,
        "whip_vs_age_level": None,
        "strikeouts_per_9_vs_age_level": None,
        "walks_per_9_vs_age_level": None,
        "hits_per_9_vs_age_level": None,
        "hr_per_9_vs_age_level": None,
        "strikeout_walk_ratio_vs_age_level": st.column_config.NumberColumn( "K/BB vs Age Level", format="%.2f", ),
    }

    return column_config
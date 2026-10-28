import pandas as pd
import streamlit as st
from processing.config import LEVEL_ORDER

batting = pd.read_parquet(
    "data/processed/historical_batting.parquet"
)

hitting_development = pd.read_parquet(
    "data/processed/hitting_development.parquet"
)

def get_all_batting_data():
    batting["level"] = pd.Categorical(
        batting["level"],
        categories = LEVEL_ORDER,
        ordered = True
    )
    return batting.sort_values(["season", "level"])

def get_seasonal_batting_data():
    return sorted(
        batting["season"].dropna().unique(),
        reverse=True,
    )

def get_level_batting_data():
    batting["level"] = pd.Categorical(
        batting["level"],
        categories = LEVEL_ORDER,
        ordered = True
    )

    return list(
        batting["level"].dropna().unique(),
    )

def get_positional_batting_data():
    return sorted(
        batting["position"].dropna().unique(),
    )

def get_hitting_development_data():
    hitting_development["level"] = pd.Categorical(
        hitting_development["level"],
        categories = LEVEL_ORDER,
        ordered = True
    )
    return hitting_development.sort_values(["season", "level"])

def get_top_hitters(batting_season, batting_level, batting_position, min_pa):
    development_columns = [
        "player_id",
        "season",
        "level",
        "ops_vs_level",
        "ops_vs_age_level",
    ]

    available_columns = [
        col for col in development_columns
        if col in hitting_development.columns
    ]

    hitter_board = batting.merge(
        hitting_development[available_columns].drop_duplicates(
            subset=["player_id", "season", "level"]
        ),
        on=["player_id", "season", "level"],
        how="left",
    )

    hitter_board = hitter_board[
        hitter_board["season"] == batting_season
    ].copy()

    if batting_level != "All":
        hitter_board = hitter_board[
            hitter_board["level"] == batting_level
        ]

    if batting_position != "All":
        hitter_board = hitter_board[
            hitter_board["position"] == batting_position
        ]

    hitter_board = hitter_board[
        hitter_board["pa"] >= min_pa
    ].copy()

    hitter_board = hitter_board.sort_values(
        "ops_vs_level",
        ascending=False,
        na_position="last",
    )

    return hitter_board

def get_basic_batting_column_config():
    column_config={
        "player_id": None,
        "player_name": "Player Name",
        "team_id": None,
        "team_name": "Team Name",
        "season": "Season",
        "league": None,
        "level": "Level",
        "position": "Position",
        "age": "Age",
        "games": None,
        "plate_appearances": "PA",
        "at_bats": None,
        "hits": None,
        "runs": None,
        "doubles": None,
        "triples": None,
        "home_runs": "HR",
        "hbp": None,
        "sac_fly": None,
        "sac_bunt": None,
        "walks": None,
        "strikeouts": None,
        "hbp": None,
        "sac_fly": None,
        "sac_bunt": None,
        "rbi": None,
        "stolen_bases": "SB",
        "caught_stealing": "CS",
        "avg": st.column_config.NumberColumn( "BA", format="%.3f", ),
        "obp": st.column_config.NumberColumn( "OBP", format="%.3f", ),
        "slg": st.column_config.NumberColumn( "SLG", format="%.3f", ),
        "ops": st.column_config.NumberColumn( "OPS", format="%.3f", ),
        "babip": None,
        "total_bases": None,
        "pa": None,
        "k_rate": st.column_config.NumberColumn( "K%", format="%.4f", step=0.0001),
        "bb_rate": st.column_config.NumberColumn( "BB%", format="%.4f", step=0.0001),
        "iso": st.column_config.NumberColumn( "ISO", format="%.3f", ),
        "sample_size_category": None,
    }

    return column_config

def get_top_hitters_column_config():
    column_config={
        "player_id": None,
        "player_name": "Player",
        "age": "Age",
        "position": "Position",
        "level": "Level",
        "pa": st.column_config.NumberColumn(
            "PA",
            format="%d",
        ),
        "ops": st.column_config.NumberColumn(
            "OPS",
            format="%.3f",
        ),
        "ops_vs_level": st.column_config.NumberColumn(
            "OPS vs Level",
            format="%+.3f",
            help="Player OPS minus the overall level baseline.",
        ),
        "ops_vs_age_level": st.column_config.NumberColumn(
            "OPS vs Age/Level",
            format="%+.3f",
            help="Player OPS minus the age-and-level baseline.",
        ),
    }
    return column_config

def get_hitter_baseline_comparison_column_config():
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
        "plate_appearances": "PA",
        "at_bats": None,
        "hits": None,
        "runs": None,
        "doubles": None,
        "triples": None,
        "home_runs": None,
        "hbp": None,
        "sac_fly": None,
        "sac_bunt": None,
        "walks": None,
        "strikeouts": None,
        "rbi": None,
        "stolen_bases": None,
        "caught_stealing": None,
        "avg": None,
        "obp": None,
        "slg": None,
        "ops": "OPS",
        "babip": None,
        "total_bases": None,
        "pa": None,
        "k_rate": None,
        "bb_rate": None,
        "iso": None,
        "sample_size_category": None,
        "level_players": None,
        "level_plate_appearances": None,
        "level_avg": None,
        "avg_vs_level": None,
        "level_obp": None,
        "obp_vs_level": None,
        "level_slg": None,
        "slg_vs_level": None,
        "level_ops": st.column_config.NumberColumn( "Level OPS", format="%.3f", ),
        "ops_vs_level": st.column_config.NumberColumn( "OPS vs Level", format="%.3f", ),
        "level_k_rate": None,
        "k_rate_vs_level": None,
        "level_bb_rate": None,
        "bb_rate_vs_level": None,
        "level_iso": None,
        "iso_vs_level": None,
        "age_level_players": None,
        "age_level_plate_appearances": None,
        "age_level_avg": None,
        "avg_vs_age_level": None,
        "age_level_obp": None,
        "obp_vs_age_level": None,
        "age_level_slg": None,
        "slg_vs_age_level": None,
        "age_level_ops": st.column_config.NumberColumn( "Age Level OPS", format="%.3f", ),
        "ops_vs_age_level": st.column_config.NumberColumn( "OPS vs Age Level", format="%.3f", ),
        "age_level_k_rate": None,
        "k_rate_vs_age_level": None,
        "age_level_bb_rate": None,
        "bb_rate_vs_age_level": None,
        "age_level_iso": None,
        "iso_vs_age_level": None,
    }

    return column_config
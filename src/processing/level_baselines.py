import pandas as pd
from src.api.teamStats import get_all_stats_per_level
from src.processing.historical_pitching import innings_pitched_to_decimal

def create_hitting_level_baselines(sport_id, season=2026):
    df = get_all_stats_per_level(
        sport_id=sport_id,
        season=season,
        group="hitting",
        player_pool="ALL",
        stats="season"
    )
    grouped = (
        df
        .groupby(["season", "level", "age"], as_index=False)
        .agg({
            "player_id": "nunique",
            "plate_appearances": "sum",
            "at_bats": "sum",
            "hits": "sum",
            "walks": "sum",
            "hbp": "sum",
            "sac_fly": "sum",
            "strikeouts": "sum",
            "total_bases": "sum",
        })
        .rename(columns={
            "player_id": "players",
        })
    )

    grouped["avg"] = grouped["hits"] / grouped["at_bats"]
    grouped["obp"] = (
        grouped["hits"] + grouped["walks"] + grouped["hbp"]) / (
        grouped["at_bats"] + grouped["walks"] + grouped["hbp"] + grouped["sac_fly"])
    grouped["slg"] = grouped["total_bases"] / grouped["at_bats"]
    grouped["ops"] = grouped["obp"] + grouped["slg"]
    grouped["iso"] = grouped["slg"] - grouped["avg"]
    grouped["k_rate"] = grouped["strikeouts"] / grouped["plate_appearances"]
    grouped["bb_rate"] = grouped["walks"] / grouped["plate_appearances"]
    return grouped

def create_pitching_level_baselines(sport_id, season=2026):
    df = get_all_stats_per_level(
        sport_id=sport_id,
        season=season,
        group="pitching",
        player_pool="ALL",
        stats="season"
    )
    df["ip_decimal"] = df["innings_pitched"].apply(innings_pitched_to_decimal)
    grouped = (
        df
        .groupby(["season", "level", "age"], as_index=False)
        .agg({
            "player_id": "nunique",
            "ip_decimal": "sum",
            "hits_allowed": "sum",
            "walks": "sum",
            "strikeouts": "sum",
            "runs_allowed": "sum",
            "home_runs_allowed": "sum",
            "earned_runs": "sum",
        })
        .rename(columns={
            "player_id": "players",
            "ip_decimal": "innings_pitched",
        })
    )

    grouped["era"] = grouped["earned_runs"] / grouped["innings_pitched"] * 9
    grouped["whip"] = (
        grouped["hits_allowed"] + grouped["walks"]) / (
        grouped["innings_pitched"])
    grouped["strikeouts_per_9"] = grouped["strikeouts"] / grouped["innings_pitched"] * 9
    grouped["walks_per_9"] = grouped["walks"] / grouped["innings_pitched"] * 9
    grouped["hits_per_9"] = grouped["hits_allowed"] / grouped["innings_pitched"] * 9
    grouped["strikeout_walk_ratio"] = grouped["strikeouts"] / grouped["walks"]
    grouped["hr_per_9"] = grouped["home_runs_allowed"] / grouped["innings_pitched"] * 9
    return grouped
from src.api.teamStats import get_current_cardinals_milb_history
import pandas as pd
from src.processing.config import TEAM_ID, START_SEASON, END_SEASON, TEAM_LEVELS

def createPitchingDataTables(team_id=TEAM_ID, start_season=START_SEASON, end_season=END_SEASON):
    historical_pitching = get_current_cardinals_milb_history(parent_team_id=team_id, group="pitching",start_season=start_season, end_season=end_season)
    historical_pitching["ip_decimal"] = historical_pitching[
        "innings_pitched"
    ].apply(innings_pitched_to_decimal)
    for metric in ["era", "whip", "strikeouts_per_9", "walks_per_9", "hits_per_9", "strikeout_walk_ratio"]:
        historical_pitching[metric] = pd.to_numeric(
            historical_pitching[metric],
            errors="coerce",
        )

    historical_pitching["hr_per_9"] = (historical_pitching["home_runs_allowed"] / historical_pitching["ip_decimal"].replace(0, pd.NA) * 9)
    # historical_pitching["sample_size"] = historical_pitching["innings_pitched"].apply(classify_sample_size)
    return historical_pitching

def innings_pitched_to_decimal(ip):
    if pd.isna(ip):
        return pd.NA

    whole, remainder = str(ip).split(".")

    whole = int(whole)
    remainder = int(remainder)

    if remainder == 0:
        return whole
    elif remainder == 1:
        return whole + (1 / 3)
    elif remainder == 2:
        return whole + (2 / 3)
    else:
        raise ValueError(f"Unexpected innings pitched value: {ip}")
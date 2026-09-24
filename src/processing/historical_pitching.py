from src.api.teamStats import get_cardinals_minor_league_stats
import pandas as pd
from src.processing.config import TEAM_ID, SEASONS, TEAM_LEVELS

def createPitchingDataTables(team_id=TEAM_ID, seasons=SEASONS):
    historical_pitching = get_cardinals_minor_league_stats(team_id, group="pitching", seasons=seasons)
    historical_pitching["ip_decimal"] = historical_pitching[
        "innings_pitched"
    ].apply(innings_pitched_to_decimal)
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
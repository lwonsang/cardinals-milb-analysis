from src.api.teamStats import get_cardinals_minor_league_stats
import pandas as pd
from src.processing.config import TEAM_ID, SEASONS, TEAM_LEVELS

def createBattingDataTables(team_id=TEAM_ID, seasons=SEASONS):
    historical_batting = get_cardinals_minor_league_stats(team_id, group="hitting", seasons=seasons)
    historical_batting["pa"] = pd.to_numeric(
        historical_batting["plate_appearances"], errors="coerce"
    )

    historical_batting["strikeouts"] = pd.to_numeric(
        historical_batting["strikeouts"], errors="coerce"
    )

    historical_batting["walks"] = pd.to_numeric(
        historical_batting["walks"], errors="coerce"
    )

    historical_batting["avg"] = pd.to_numeric(historical_batting["avg"], errors="coerce")
    historical_batting["slg"] = pd.to_numeric(historical_batting["slg"], errors="coerce")

    historical_batting["k_rate"] = historical_batting["strikeouts"] / historical_batting["pa"].replace(0, pd.NA)
    historical_batting["bb_rate"] = historical_batting["walks"] / historical_batting["pa"].replace(0, pd.NA)
    historical_batting["iso"] = historical_batting["slg"] - historical_batting["avg"]

    historical_batting["sample_size_category"] = historical_batting["plate_appearances"].apply(classify_sample_size)
    return historical_batting

def classify_sample_size(pa):
    if pa < 25:
        return "Very small"
    elif pa < 50:
        return "Small"
    elif pa < 100:
        return "Moderate"
    else:
        return "Large"
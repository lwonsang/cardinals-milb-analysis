from src.api.teamStats import get_current_cardinals_milb_history
import pandas as pd
from src.processing.config import TEAM_ID, START_SEASON, END_SEASON

def createBattingDataTables(team_id=TEAM_ID, start_season=START_SEASON, end_season=END_SEASON):
    historical_batting = get_current_cardinals_milb_history(parent_team_id=team_id, group="hitting", start_season=start_season, end_season=end_season)
    historical_batting["pa"] = pd.to_numeric(
        historical_batting["plate_appearances"], errors="coerce"
    )
    for metric in ["strikeouts", "walks", "avg", "obp", "slg", "ops"]:
        historical_batting[metric] = pd.to_numeric(
            historical_batting[metric],
            errors="coerce",
        )

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
from src.processing.config import TEAM_ID, START_SEASON, END_SEASON, MINOR_LEAGUE_LEVELS
from src.processing.historical_batting import createBattingDataTables
from src.processing.historical_pitching import createPitchingDataTables
from src.processing.current_status import createCurrentStatus
from src.processing.playerDevelopmentTables import createPlayerDevelopmentTable
from src.processing.level_baselines import create_hitting_level_baselines, create_pitching_level_baselines
from src.processing.baseline_comparison_metrics import create_hitting_baseline_comparison_metrics, create_pitching_baseline_comparison_metrics
from src.api.teamStats import (
    get_current_minor_league_rosters,
    get_current_major_league_roster,
)
from pathlib import Path
import pandas as pd

PROCESSED_DATA_DIR = Path("data/processed")
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def build_dataset(team_id=TEAM_ID, start_season=START_SEASON, end_season=END_SEASON):
    historical_batting = createBattingDataTables(
        team_id=team_id,
        start_season=start_season,
        end_season=end_season,
    )

    historical_pitching = createPitchingDataTables(
        team_id=team_id,
        start_season=start_season,
        end_season=end_season,
    )

    minor_league_rosters = get_current_minor_league_rosters()

    active_major_league_roster = get_current_major_league_roster(
        team_id,
        rosterType="active",
    )

    forty_man_major_league_roster = get_current_major_league_roster(
        team_id,
        rosterType="40Man",
    )

    current_status = createCurrentStatus(
        minor_league_rosters,
        active_major_league_roster,
        forty_man_major_league_roster,
    )

    player_development = createPlayerDevelopmentTable(
        historical_batting,
        historical_pitching,
        current_status,
    )

    hitting_level_baselines = []
    pitching_level_baselines = []

    hitting_level_baselines_by_age = []
    pitching_level_baselines_by_age = []
    age_categories = ["season", "level", "age"]

    for season in range(start_season, end_season + 1):
        for sport_id in MINOR_LEAGUE_LEVELS:
            hitting_level_baselines.append(create_hitting_level_baselines(sport_id, season=season))
            pitching_level_baselines.append(create_pitching_level_baselines(sport_id, season=season))
            hitting_level_baselines_by_age.append(create_hitting_level_baselines(sport_id, season=season, group_by=age_categories))
            pitching_level_baselines_by_age.append(create_pitching_level_baselines(sport_id, season=season, group_by=age_categories))

    hitting_level_baselines = pd.concat(
        hitting_level_baselines,
        ignore_index=True,
    )
    hitting_level_baselines_by_age = pd.concat(
        hitting_level_baselines_by_age,
        ignore_index=True,
    )
    pitching_level_baselines = pd.concat(
        pitching_level_baselines,
        ignore_index=True,
    )
    pitching_level_baselines_by_age = pd.concat(
        pitching_level_baselines_by_age,
        ignore_index=True,
    )

    hitting_development = create_hitting_baseline_comparison_metrics(
        historical_batting,
        hitting_level_baselines,
        hitting_level_baselines_by_age,
    )
    
    pitching_development = create_pitching_baseline_comparison_metrics(
        historical_pitching,
        pitching_level_baselines,
        pitching_level_baselines_by_age
    )

    return {
        "historical_batting": historical_batting,
        "historical_pitching": historical_pitching,
        "current_status": current_status,
        "player_development": player_development,
        "hitting_level_baselines": hitting_level_baselines,
        "pitching_level_baselines": pitching_level_baselines,
        "hitting_level_baselines_by_age": hitting_level_baselines_by_age,
        "pitching_level_baselines_by_age": pitching_level_baselines_by_age,
        "hitting_development": hitting_development,
        "pitching_development": pitching_development
    }

if __name__ == "__main__":
    datasets = build_dataset()

    datasets["historical_batting"].to_parquet(
        PROCESSED_DATA_DIR / "historical_batting.parquet",
        index=False,
    )

    datasets["historical_pitching"].to_parquet(
        PROCESSED_DATA_DIR / "historical_pitching.parquet",
        index=False,
    )

    datasets["current_status"].to_parquet(
        PROCESSED_DATA_DIR / "current_status.parquet",
        index=False,
    )

    datasets["hitting_development"].to_parquet(
        PROCESSED_DATA_DIR / "hitting_development.parquet",
        index=False,
    )

    datasets["pitching_development"].to_parquet(
        PROCESSED_DATA_DIR / "pitching_development.parquet",
        index=False,
    )

    print("Dataset build complete.")
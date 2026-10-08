import pandas as pd

HITTING_RATE_METRICS = [
    "avg",
    "obp",
    "slg",
    "ops",
    "iso",
    "k_rate",
    "bb_rate",
]
PITCHING_RATE_METRICS = [
    "era",
    "whip",
    "strikeouts_per_9",
    "walks_per_9",
    "hits_per_9",
    "strikeout_walk_ratio",
    "hr_per_9",
]

def create_hitting_baseline_comparison_metrics(
    batting,
    level_baselines,
    age_level_baselines,
):
    development = batting.copy()
    level_baselines = level_baselines.rename(
        columns={
            "players": "level_players",
            "plate_appearances": "level_plate_appearances",
            **{
                metric: f"level_{metric}"
                for metric in HITTING_RATE_METRICS
            },
        }
    )

    level_columns = [
        "season",
        "level",
        "level_players",
        "level_plate_appearances",
        *[
            f"level_{metric}"
            for metric in HITTING_RATE_METRICS
        ],
    ]

    development = development.merge(
        level_baselines[level_columns],
        on=["season", "level"],
        how="left",
        validate="many_to_one",
    )

    age_level_baselines = age_level_baselines.rename(
        columns={
            "players": "age_level_players",
            "plate_appearances": "age_level_plate_appearances",
            **{
                metric: f"age_level_{metric}"
                for metric in HITTING_RATE_METRICS
            },
        }
    )

    age_level_columns = [
        "season",
        "level",
        "age",
        "age_level_players",
        "age_level_plate_appearances",
        *[
            f"age_level_{metric}"
            for metric in HITTING_RATE_METRICS
        ],
    ]

    development = development.merge(
        age_level_baselines[age_level_columns],
        on=["season", "level", "age"],
        how="left",
        validate="many_to_one",
    )

    for metric in HITTING_RATE_METRICS:
        development[f"{metric}_vs_level"] = (
            development[metric]
            - development[f"level_{metric}"]
        )

        development[f"{metric}_vs_level"] = pd.to_numeric(
            development[f"{metric}_vs_level"],
            errors="coerce",
        )

        development[f"{metric}_vs_age_level"] = (
            development[metric]
            - development[f"age_level_{metric}"]
        )

        development[f"{metric}_vs_age_level"] = pd.to_numeric(
            development[f"{metric}_vs_age_level"],
            errors="coerce",
        )

    return development

def create_pitching_baseline_comparison_metrics(
    pitching,
    level_baselines,
    age_level_baselines,
):
    development = pitching.copy()
    level_baselines = level_baselines.rename(
        columns={
            "players": "level_players",
            "innings_pitched": "level_innings_pitched",
            **{
                metric: f"level_{metric}"
                for metric in PITCHING_RATE_METRICS
            },
        }
    )

    level_columns = [
        "season",
        "level",
        "level_players",
        "level_innings_pitched",
        *[
            f"level_{metric}"
            for metric in PITCHING_RATE_METRICS
        ],
    ]

    development = development.merge(
        level_baselines[level_columns],
        on=["season", "level"],
        how="left",
        validate="many_to_one",
    )

    age_level_baselines = age_level_baselines.rename(
        columns={
            "players": "age_level_players",
            "innings_pitched": "age_level_innings_pitched",
            **{
                metric: f"age_level_{metric}"
                for metric in PITCHING_RATE_METRICS
            },
        }
    )

    age_level_columns = [
        "season",
        "level",
        "age",
        "age_level_players",
        "age_level_innings_pitched",
        *[
            f"age_level_{metric}"
            for metric in PITCHING_RATE_METRICS
        ],
    ]

    development = development.merge(
        age_level_baselines[age_level_columns],
        on=["season", "level", "age"],
        how="left",
        validate="many_to_one",
    )

    for metric in PITCHING_RATE_METRICS:
        development[f"{metric}_vs_level"] = (
            development[metric]
            - development[f"level_{metric}"]
        )

        development[f"{metric}_vs_level"] = pd.to_numeric(
            development[f"{metric}_vs_level"],
            errors="coerce",
        )

        development[f"{metric}_vs_age_level"] = (
            development[metric]
            - development[f"age_level_{metric}"]
        )

        development[f"{metric}_vs_age_level"] = pd.to_numeric(
            development[f"{metric}_vs_age_level"],
            errors="coerce",
        )

    return development

import csv
import pandas as pd
from collections import defaultdict
from teamStats import get_cardinals_minor_league_stats, get_current_minor_league_rosters, get_current_major_league_roster

MIN_PA = 50
TEAM_ID = 138
SEASONS = [2025,2026]

def createPlayerDevelopmentTable(historical_batting, historical_pitching, current_status):
    players = {}
    batting_player_ids = set(historical_batting["player_id"])
    pitching_player_ids = set(historical_pitching["player_id"])

    player_ids = batting_player_ids | pitching_player_ids

    for player_id in player_ids:
        batting_group = historical_batting[
            historical_batting["player_id"] == player_id
        ]

        pitching_group = historical_pitching[
            historical_pitching["player_id"] == player_id
        ]

        player_status = current_status[
            current_status["player_id"] == player_id
        ]

        if not batting_group.empty:
            player_name = batting_group["player_name"].iloc[0]
        elif not pitching_group.empty:
            player_name = pitching_group["player_name"].iloc[0]
        else:
            player_name = "Unknown"

        if not player_status.empty:
            status = player_status.iloc[0]

            current_status_data = {
                "organization_status": status["organization_status"],
                "current_level": status["current_level"],
                "status_code": status["status_code"],
                "status_description": status["status_description"],
            }
        else:
            current_status_data = {
                "organization_status": "Not currently on Cardinals roster",
                "current_level": None,
                "status_code": None,
                "status_description": None,
            }

        players[player_id] = {
            "player_id": player_id,
            "name": player_name,

            "current_status": current_status_data,

            "hitting": {
                "stints": batting_group[
                    [
                        "team_id",
                        "team_name",
                        "season",
                        "level",
                        "league",
                        "age",
                        "plate_appearances",
                        "avg",
                        "obp",
                        "slg",
                        "ops",
                        "k_rate",
                        "bb_rate",
                        "iso",
                    ]
                ].to_dict("records")
            },

            "pitching": {
                "stints": pitching_group[
                    [
                        "team_id",
                        "team_name",
                        "season",
                        "level",
                        "league",
                        "age",
                        "innings_pitched",
                        "era",
                        "whip",
                        "strikeouts_per_9",
                        "walks_per_9",
                        "hr_per_9",
                    ]
                ].to_dict("records")
            }
        }
        print(players[player_id])

    return players

def createCurrentStatus(minors, active, fortyman):
    rows = []
    player_ids = set(minors["player_id"]) \
        | set(active["player_id"]) \
        | set(fortyman["player_id"])

    for player_id in player_ids:
        active_match = active[active["player_id"] == player_id]
        if not active_match.empty:
            player = active_match.iloc[0]
            rows.append({
                "player_id": player["player_id"],
                "player_name": player["player_name"],
                "organization_status": "MLB Active",
                "team_id": player["team_id"],
                "current_level": "MLB",
                "position": player["position"],
                "status_code": player["status_code"],
                "status_description": player["status_description"],
                "parent_team_id": player["parent_team_id"]
            })
            continue

        minor_match = minors[minors["player_id"] == player_id]
        if not minor_match.empty:
            player = resolve_minor_league_status(minor_match)
            rows.append({
                "player_id": player["player_id"],
                "player_name": player["player_name"],
                "organization_status": "Cardinals Minor Leagues",
                "team_id": player["team_id"],
                "current_level": player["current_level"],
                "position": player["position"],
                "status_code": player["status_code"],
                "status_description": player["status_description"],
                "parent_team_id": player["parent_team_id"]
            })
            continue

        forty_match = fortyman[fortyman["player_id"] == player_id]
        if not forty_match.empty:
            player = forty_match.iloc[0]
            rows.append({
                "player_id": player["player_id"],
                "player_name": player["player_name"],
                "organization_status": "Cardinals 40-Man Roster",
                "team_id": player["team_id"],
                "current_level": "MLB",
                "position": player["position"],
                "status_code": player["status_code"],
                "status_description": player["status_description"],
                "parent_team_id": player["parent_team_id"]
            })
            continue
    return pd.DataFrame(rows)

def createBattingDataTables():
    historical_batting = get_cardinals_minor_league_stats(TEAM_ID, seasons=SEASONS)
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

    historical_batting["sample_size"] = historical_batting["plate_appearances"].apply(classify_sample_size)
    
    historical_batting.to_csv("cardinals_milb_batters.csv", index=False)
    return historical_batting

def createPitchingDataTables():
    historical_pitching = get_cardinals_minor_league_stats(TEAM_ID, group="pitching", seasons=SEASONS)
    historical_pitching["ip_decimal"] = historical_pitching[
        "innings_pitched"
    ].apply(innings_pitched_to_decimal)
    historical_pitching["hr_per_9"] = (historical_pitching["home_runs_allowed"] / historical_pitching["ip_decimal"].replace(0, pd.NA) * 9)
    # historical_pitching["sample_size"] = historical_pitching["innings_pitched"].apply(classify_sample_size)
    historical_pitching.to_csv("cardinals_milb_pitchers.csv", index=False)
    return historical_pitching

def createPlayerSummary(historical_batting):
    player_summary = (
        historical_batting
        .groupby(["player_id", "player_name"])
        .agg(
            levels=("level", list),
            total_pa=("plate_appearances", "sum"),
            num_levels=("level", "nunique"),
        )
        .reset_index()
    )
    # print(player_summary.head())
    # print(player_summary.shape)
    return player_summary

def createQualifiedRankings(historical_batting):
    qualified_df = historical_batting[historical_batting["pa"] >= MIN_PA]
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

def resolve_minor_league_status(player_records):
    active = player_records[
        player_records["status_code"] == "A"
    ]
    if not active.empty:
        return active.iloc[0]

    rehab = player_records[
        player_records["status_code"] == "RA"
    ]
    if not rehab.empty:
        return rehab.iloc[0]

    development = player_records[
        player_records["status_code"] == "DEV"
    ]
    if not development.empty:
        return development.iloc[0]

    return player_records.iloc[0]

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

if __name__ == "__main__":
    historical_batting = createBattingDataTables()
    historical_pitching = createPitchingDataTables()
    minor_league_rosters = get_current_minor_league_rosters()
    minor_league_rosters.to_csv("minors.csv", index=False)
    active_major_league_roster = get_current_major_league_roster(TEAM_ID, rosterType="active")
    forty_man_major_league_roster = get_current_major_league_roster(TEAM_ID, rosterType="40Man")
    active_major_league_roster.to_csv("active.csv", index=False)
    forty_man_major_league_roster.to_csv("forty_man.csv", index=False)
    current_status = createCurrentStatus(minor_league_rosters, active_major_league_roster, forty_man_major_league_roster)
    player_development_table = createPlayerDevelopmentTable(historical_batting, historical_pitching, current_status)
    createPlayerSummary(historical_batting)
    createQualifiedRankings(historical_batting)
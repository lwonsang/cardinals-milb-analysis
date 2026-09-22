import csv
import pandas as pd
from collections import defaultdict
from teamStats import get_cardinals_minor_league_stats, get_current_minor_league_rosters, get_current_major_league_roster

MIN_PA = 50
TEAM_ID = 138

def createPlayerDevelopmentTable(historical_records, current_status):
    players = {}

    for player_id, group in historical_records.groupby("player_id"):

        player_status = current_status[
            current_status["player_id"] == player_id
        ]

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
            "name": group["player_name"].iloc[0],

            "current_status": current_status_data,

            "stints": group[
                [
                    "team_id",
                    "team_name",
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
        }
        # print(players[player_id])

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

def createDataTables():
    historical_records = get_cardinals_minor_league_stats(TEAM_ID)
    historical_records["pa"] = pd.to_numeric(
        historical_records["plate_appearances"], errors="coerce"
    )

    historical_records["strikeouts"] = pd.to_numeric(
        historical_records["strikeouts"], errors="coerce"
    )

    historical_records["walks"] = pd.to_numeric(
        historical_records["walks"], errors="coerce"
    )

    historical_records["avg"] = pd.to_numeric(historical_records["avg"], errors="coerce")
    historical_records["slg"] = pd.to_numeric(historical_records["slg"], errors="coerce")

    historical_records["k_rate"] = historical_records["strikeouts"] / historical_records["pa"].replace(0, pd.NA)
    historical_records["bb_rate"] = historical_records["walks"] / historical_records["pa"].replace(0, pd.NA)
    historical_records["iso"] = historical_records["slg"] - historical_records["avg"]

    historical_records["sample_size"] = historical_records["plate_appearances"].apply(classify_sample_size)
    
    historical_records.to_csv("cardinals.csv", index=False)
    return historical_records

def createPlayerSummary(historical_records):
    player_summary = (
        historical_records
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

def createQualifiedRankings(historical_records):
    qualified_df = historical_records[historical_records["pa"] >= MIN_PA]
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

if __name__ == "__main__":
    historical_records = createDataTables()
    minor_league_rosters = get_current_minor_league_rosters()
    minor_league_rosters.to_csv("minors.csv", index=False)
    active_major_league_roster = get_current_major_league_roster(TEAM_ID, rosterType="active")
    forty_man_major_league_roster = get_current_major_league_roster(TEAM_ID, rosterType="40Man")
    active_major_league_roster.to_csv("active.csv", index=False)
    forty_man_major_league_roster.to_csv("forty_man.csv", index=False)
    current_status = createCurrentStatus(minor_league_rosters, active_major_league_roster, forty_man_major_league_roster)
    player_development_table = createPlayerDevelopmentTable(historical_records, current_status)
    createPlayerSummary(historical_records)
    createQualifiedRankings(historical_records)
    for player_id in [823787, 699024, 663457]:
        print(player_development_table[player_id])

import pandas as pd

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
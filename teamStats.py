import requests
import pandas as pd

MIN_PA = 50
TEAM_ID = 138
TEAM_LEVELS = {235: "AAA", 440: "AA", 443: "A+", 279: "A"}

def get_cardinals_minor_league_stats(team_id, season=2026, player_pool="ALL"):
    affiliates = get_team_affiliates(team_id, season=season)

    target_sports = {11, 12, 13, 14}

    all_stats = []

    for team_id, team in affiliates.items():

        sport_id = team["sport"]["id"]

        if sport_id not in target_sports:
            continue

        print(f"Getting {team['name']}...")

        data = get_team_stats(
            team_id,
            season=season,
            group="hitting",
            player_pool=player_pool
        )

        df = stats_to_dataframe(data)

        all_stats.append(df)

    return pd.concat(all_stats, ignore_index=True)

def get_team_affiliates(team_id, season=2026):
    response = requests.get(
        f'https://statsapi.mlb.com/api/v1/teams/{team_id}/affiliates',
        params={'season': season}
    )
    response.raise_for_status()

    teams = response.json()['teams']

    return {
        team['id']:
        {
            'name': team['name'],
            'abbreviation': team['abbreviation'],
            'sport': {
                'id': team['sport']['id'],
                'name': team['sport']['name']
            },
            'league': team.get('league', {}).get('name')
        }
        for team in teams
    }

def get_current_roster(team_id, season=2026, rosterType='fullRoster'):
    response = requests.get(
        f'https://statsapi.mlb.com/api/v1/teams/{team_id}/roster',
        params={
            'season': season,
            'rosterType': rosterType,
            'hydrate': 'person'
        }
    )
    response.raise_for_status()

    return response.json()['roster']

def get_current_minor_league_rosters(season=2026):
    rows = []

    for team_id, level in TEAM_LEVELS.items():
        data = get_current_roster(team_id, season=season)

        for player in data:
            position = player.get("position", {})
            status = player.get("status", {})

            rows.append({
                "player_id": player["person"]["id"],
                "player_name": player["person"]["fullName"],
                "team_id": team_id,
                "current_level": level,
                "position": position.get("abbreviation"),
                "status_code": status.get("code"),
                "status_description": status.get("description"),
                "parent_team_id": player.get("parentTeamId")
            })

    return pd.DataFrame(rows)

def get_current_major_league_roster(team_id, season=2026, rosterType='active'):
    rows = []
    data = get_current_roster(team_id, season=season, rosterType=rosterType)
    
    for player in data:
        position = player.get("position", {})
        status = player.get("status", {})

        rows.append({
            "player_id": player["person"]["id"],
            "player_name": player["person"]["fullName"],
            "team_id": team_id,
            "current_level": "MLB",
            "position": position.get("abbreviation"),
            "status_code": status.get("code"),
            "status_description": status.get("description"),
            "parent_team_id": player.get("parentTeamId")
        })

    return pd.DataFrame(rows)

def get_team_stats(team_id, season=2026, group="hitting", player_pool="ALL"):
    response = requests.get(
        "https://statsapi.mlb.com/api/v1/stats",
        params={
            "stats": "season",
            "group": group,
            "season": season,
            "teamId": team_id,
            "playerPool": player_pool
        }
    )

    response.raise_for_status()
    return response.json()


def stats_to_dataframe(data):
    rows = []

    for stat_group in data["stats"]:
        for split in stat_group["splits"]:

            stat = split["stat"]
            player = split["player"]
            team = split["team"]
            sport = split["sport"]
            position = split.get("position", {})

            row = {
                "player_id": player["id"],
                "player_name": player["fullName"],
                "team_id": team["id"],
                "team_name": team["name"],
                "league": split["league"]["name"],
                "level": sport["abbreviation"],
                "position": position.get("abbreviation"),
                "age": stat.get("age"),

                "games": stat.get("gamesPlayed"),
                "plate_appearances": stat.get("plateAppearances"),
                "at_bats": stat.get("atBats"),

                "hits": stat.get("hits"),
                "runs": stat.get("runs"),
                "doubles": stat.get("doubles"),
                "triples": stat.get("triples"),
                "home_runs": stat.get("homeRuns"),
                "rbi": stat.get("rbi"),

                "walks": stat.get("baseOnBalls"),
                "strikeouts": stat.get("strikeOuts"),

                "avg": stat.get("avg"),
                "obp": stat.get("obp"),
                "slg": stat.get("slg"),
                "ops": stat.get("ops"),

                "stolen_bases": stat.get("stolenBases"),
                "caught_stealing": stat.get("caughtStealing"),

                "babip": stat.get("babip"),
                "total_bases": stat.get("totalBases"),
            }

            rows.append(row)

    return pd.DataFrame(rows)


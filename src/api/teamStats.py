import requests
import pandas as pd

MIN_PA = 50
TEAM_ID = 138
TEAM_LEVELS = {235: "AAA", 440: "AA", 443: "A+", 279: "A"}

def get_cardinals_minor_league_stats(team_id, group="hitting", seasons=None, player_pool="ALL"):
    if seasons is None:
        seasons = [2026]

    target_sports = {11, 12, 13, 14}
        
    all_stats = []

    for season in seasons:
        affiliates = get_team_affiliates(team_id, season=season)
    
        for affiliate_id, team in affiliates.items():
    
            sport_id = team["sport"]["id"]
    
            if sport_id not in target_sports:
                continue
    
            # print(f"Getting {team['name']}...")
    
            data = get_team_stats(
                affiliate_id,
                season=season,
                group=group,
                player_pool=player_pool
            )
    
            if group == "hitting":
                df = batting_stats_to_dataframe(data, season)
            elif group == "pitching":
                df = pitching_stats_to_dataframe(data, season)
            else:
                raise ValueError(f"Invalid group: {group}")
    
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

def get_current_minor_league_rosters(team_levels=TEAM_LEVELS, season=2026):
    rows = []

    for team_id, level in team_levels.items():
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
            "playerPool": player_pool,
            "limit": 1000
        }
    )

    response.raise_for_status()
    return response.json()


def batting_stats_to_dataframe(data, season):
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
                "season": season,
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

def pitching_stats_to_dataframe(data, season):
    rows = []

    for stat_group in data["stats"]:
        for split in stat_group["splits"]:

            stat = split["stat"]
            player = split["player"]
            team = split["team"]
            sport = split["sport"]

            rows.append({
                "player_id": player["id"],
                "player_name": player["fullName"],
                "team_id": team["id"],
                "team_name": team["name"],
                "season": season,
                "league": split["league"]["name"],
                "level": sport["abbreviation"],
                "position": split.get("position", {}).get("abbreviation"),
                "age": stat.get("age"),

                "games": stat.get("gamesPlayed"),
                "games_started": stat.get("gamesStarted"),

                "wins": stat.get("wins"),
                "losses": stat.get("losses"),

                "innings_pitched": stat.get("inningsPitched"),

                "hits_allowed": stat.get("hits"),
                "runs_allowed": stat.get("runs"),
                "earned_runs": stat.get("earnedRuns"),
                "home_runs_allowed": stat.get("homeRuns"),

                "walks": stat.get("baseOnBalls"),
                "strikeouts": stat.get("strikeOuts"),

                "era": stat.get("era"),
                "whip": stat.get("whip"),

                "strikeouts_per_9": stat.get("strikeoutsPer9Inn"),
                "walks_per_9": stat.get("walksPer9Inn"),
                "hits_per_9": stat.get("hitsPer9Inn"),
                "strikeout_walk_ratio": stat.get("strikeoutWalkRatio"),

                "saves": stat.get("saves"),
                "holds": stat.get("holds"),
            })

    return pd.DataFrame(rows)
import requests
import pandas as pd

MIN_PA = 50
TEAM_ID = 138
TEAM_LEVELS = {235: "AAA", 440: "AA", 443: "A+", 279: "A"}
MINOR_LEAGUE_LEVELS = {11: "AAA", 12: "AA", 13: "A+", 14: "A"}

def get_current_cardinals_milb_history(parent_team_id=TEAM_ID, group="hitting", start_season=2026, end_season=2026, player_pool="ALL"):
    current_minor_league_players = get_current_minor_league_rosters(team_levels=TEAM_LEVELS, season=end_season)

    current_player_ids = set(
        current_minor_league_players["player_id"]
    )

    seasons = list(range(start_season, end_season + 1))
    all_stats = []
    for season in seasons:
        affiliates = get_team_affiliates(parent_team_id, season=season)
        for team_id, team_info in affiliates.items():
            if team_info["sport"]["id"] not in {
                11, 12, 13, 14
            }:
                continue

            stats = get_team_stats(
                team_id,
                group=group,
                season=season,
                player_pool=player_pool
            )

            splits = stats["stats"][0]["splits"]

            for split in splits:
                player_id = split["player"]["id"]

                if player_id not in current_player_ids:
                    continue

                if group=="hitting":
                    row = normalize_batting_stats(split, season=season, level=team_info["sport"]["name"])
                elif group=="pitching":
                    row = normalize_pitching_stats(split, season=season, level=team_info["sport"]["name"])

                all_stats.append(row)

    return pd.DataFrame(all_stats)

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

def get_team_stats(team_id, season=2026, group="hitting", player_pool="ALL", stats="season", sport_id=None, limit=1000):
    response = requests.get(
        "https://statsapi.mlb.com/api/v1/stats",
        params={
            "stats": "season",
            "group": group,
            "season": season,
            "teamId": team_id,
            "sportIds": sport_id,
            "playerPool": player_pool,
            "limit": 1000
        }
    )

    response.raise_for_status()
    return response.json()

def get_team_ids_for_level(sport_id, season=2026):
    team_list = []

    response = requests.get(
        "https://statsapi.mlb.com/api/v1/teams",
        params={
            "sportId": sport_id,
            "season": season
        }
    )

    response.raise_for_status()

    for team in response.json()['teams']:
        team_list.append(team['id'])

    return team_list

def get_all_stats_per_level(sport_id, season=2026, group="hitting", player_pool="ALL", stats="season"):
    all_stats = []
    for team_id in get_team_ids_for_level(sport_id, season=season):
        stats = get_team_stats(
            team_id,
            group=group,
            season=season,
            player_pool=player_pool
        )

        splits = stats["stats"][0]["splits"]

        for split in splits:
            if group=="hitting":
                row = normalize_batting_stats(split, season=season, level=MINOR_LEAGUE_LEVELS[sport_id])
            elif group=="pitching":
                row = normalize_pitching_stats(split, season=season, level=MINOR_LEAGUE_LEVELS[sport_id])

            all_stats.append(row)

    return pd.DataFrame(all_stats)

def normalize_batting_stats(split, season, level):
    stat = split["stat"]
    player = split["player"]
    team = split["team"]
    sport = split["sport"]
    position = split.get("position", {})

    return {
        "player_id": player["id"],
        "player_name": player["fullName"],
        "team_id": team["id"],
        "team_name": team["name"],
        "season": season,
        "league": split["league"]["name"],
        "level": level,
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

        "hbp": stat.get("hitByPitch"),
        "sac_fly": stat.get("sacFly"),
        "sac_bunt": stat.get("sacBunt"),

        "avg": stat.get("avg"),
        "obp": stat.get("obp"),
        "slg": stat.get("slg"),
        "ops": stat.get("ops"),

        "stolen_bases": stat.get("stolenBases"),
        "caught_stealing": stat.get("caughtStealing"),

        "babip": stat.get("babip"),
        "total_bases": stat.get("totalBases"),
    }

def normalize_pitching_stats(split, season, level):
    stat = split["stat"]
    player = split["player"]
    team = split["team"]
    sport = split["sport"]

    return{
        "player_id": player["id"],
        "player_name": player["fullName"],
        "team_id": team["id"],
        "team_name": team["name"],
        "season": season,
        "league": split["league"]["name"],
        "level": level,
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
    }
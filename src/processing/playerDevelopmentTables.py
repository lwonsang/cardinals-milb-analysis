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
        # print(players[player_id])

    return players
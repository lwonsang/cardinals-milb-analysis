import streamlit as st
import pandas as pd
import plotly.express as px

st.title("St. Louis Cardinals Minor League Player Development View")

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


batting = pd.read_parquet(
    "data/processed/historical_batting.parquet"
)

pitching = pd.read_parquet(
    "data/processed/historical_pitching.parquet"
)

status = pd.read_parquet(
    "data/processed/current_status.parquet"
)

hitters_tab, pitchers_tab = st.tabs(
    ["Hitters", "Pitchers"]
)

player_id = st.session_state.get("selected_player_id")

if st.button("← Back to Dashboard"):
    st.switch_page("app.py")

with hitters_tab:
    st.subheader("Cardinals MiLB Hitters")

    player_names = sorted(
        batting["player_name"].dropna().unique()
    )

    if player_id is not None:
        player_id = int(player_id)
        matching_players = batting[
            batting["player_id"] == player_id
        ]

        if matching_players.empty:
            st.error(
                "No matching player found for player id {}".format(player_id)
            )
            st.stop()

        selected_player = matching_players["player_name"].iloc[0]
        selected_index = player_names.index(selected_player)
    else:
        selected_index = 0

    selected_player = st.selectbox(
        "Player Name",
        player_names,
        index=selected_index,
    )

    player_batting = batting[
        batting["player_name"] == selected_player
    ].sort_values(
        ["season", "level"]
    )

    player_status = status[
        status["player_id"] == player_batting["player_id"].iloc[0]
    ]

    if player_status.empty:
        current_cardinals_player = False
    else:
        current_cardinals_player = (
            player_status.iloc[0]["organization_status"]
            != "Not currently on Cardinals roster"
        )

    st.subheader(player_batting["player_name"].iloc[-1])

    status_row = player_status.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Position",
        player_batting["position"].iloc[-1],
    )

    col2.metric(
        "Current Level",
        status_row["current_level"],
    )

    col3.metric(
        "Age",
        player_batting["age"].iloc[-1],
    )

    batting_frame = st.dataframe(
    player_batting, 
    column_config={
        "player_id": None,
        "player_name": None,
        "team_id": None,
        "team_name": "Team Name",
        "season": "Season",
        "league": None,
        "level": "Level",
        "position": "Position",
        "age": "Age",
        "games": None,
        "plate_appearances": "PA",
        "at_bats": None,
        "hits": None,
        "runs": None,
        "doubles": None,
        "triples": None,
        "home_runs": "HR",
        "walks": None,
        "strikeouts": None,
        "rbi": None,
        "stolen_bases": None,
        "caught_stealing": None,
        "avg": st.column_config.NumberColumn( "BA", format="%.3f", ),
        "obp": st.column_config.NumberColumn( "OBP", format="%.3f", ),
        "slg": st.column_config.NumberColumn( "SLG", format="%.3f", ),
        "ops": st.column_config.NumberColumn( "OPS", format="%.3f", ),
        "babip": None,
        "total_bases": None,
        "pa": None,
        "k_rate": st.column_config.NumberColumn( "K%", format="%.4f", step=0.0001),
        "bb_rate": st.column_config.NumberColumn( "BB%", format="%.4f", step=0.0001),
        "iso": st.column_config.NumberColumn( "ISO", format="%.3f", ),
        "sample_size_category": None,
    },
    use_container_width=True,
    hide_index=True
)

with pitchers_tab:
    st.subheader("Cardinals MiLB Pitchers")

    player_names = sorted(
        pitching["player_name"].dropna().unique()
    )

    if player_id is not None:
        player_id = int(player_id)
        matching_players = pitching[
            pitching["player_id"] == player_id
        ]

        if matching_players.empty:
            st.error(
                "No matching player found for player id {}".format(player_id)
            )
            st.stop()

        selected_player = matching_players["player_name"].iloc[0]
        selected_index = player_names.index(selected_player)
    else:
        selected_index = 0

    selected_player = st.selectbox(
        "Player Name",
        player_names,
        index=selected_index,
    )

    player_pitching = pitching[
        pitching["player_name"] == selected_player
    ].sort_values(
        ["season", "level"]
    )

    player_status = status[
        status["player_id"] == player_pitching["player_id"].iloc[0]
    ]

    if player_status.empty:
        current_cardinals_player = False
    else:
        current_cardinals_player = (
            player_status.iloc[0]["organization_status"]
            != "Not currently on Cardinals roster"
        )

    st.subheader(player_pitching["player_name"].iloc[-1])

    status_row = player_status.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Position",
        player_pitching["position"].iloc[-1],
    )

    col2.metric(
        "Current Level",
        status_row["current_level"],
    )

    col3.metric(
        "Age",
        player_pitching["age"].iloc[-1],
    )

    pitching_frame = st.dataframe(
        player_pitching, 
        column_config={
            "player_id": None,
            "player_name": "Player Name",
            "team_id": None,
            "team_name": "Team Name",
            "season": "Season",
            "league": None,
            "level": "Level",
            "position": None,
            "age": "Age",
            "games": None,
            "games_started": None,
            "wins": None,
            "losses": None,
            "innings_pitched": "IP",
            "hits_allowed": None,
            "runs_allowed": None,
            "earned_runs": None,
            "home_runs_allowed": None,
            "walks": None,
            "strikeouts": None,
            "era": st.column_config.NumberColumn( "ERA", format="%.2f", ),
            "whip": st.column_config.NumberColumn( "WHIP", format="%.2f", ),
            "strikeouts_per_9": st.column_config.NumberColumn( "K/9", format="%.2f", ),
            "walks_per_9": st.column_config.NumberColumn( "BB/9", format="%.2f", ),
            "hits_per_9": st.column_config.NumberColumn( "H/9", format="%.2f", ),
            "hr_per_9": st.column_config.NumberColumn( "HR/9", format="%.2f", ),
            "strikeout_walk_ratio": st.column_config.NumberColumn( "K/BB", format="%.2f", ),
            "saves": None,
            "holds": None,
            "ip_decimal": None,
        },
        use_container_width=True,
        hide_index=True
    )
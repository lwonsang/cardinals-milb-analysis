import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Cardinals Player Development",
    layout="wide",
)

st.title("St. Louis Cardinals Minor League Player Development")

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


with hitters_tab:
    st.subheader("Batting")

    col1, col2, col3, col4 = st.columns(4)

    batting_seasons = sorted(
        batting["season"].dropna().unique(),
        reverse=True,
    )

    with col1:
        batting_season = st.selectbox(
            "Season",
            batting_seasons,
            index=(
                batting_seasons.index(2026)
                if 2026 in batting_seasons
                else 0
            ),
            key="batting_season",
        )

    batting_levels = sorted(
        batting["level"].dropna().unique()
    )

    with col2:
        batting_level = st.selectbox(
            "Level",
            ["All"] + batting_levels,
            index=0,
            key="batting_level",
        )

    batting_positions = sorted(
        batting["position"].dropna().unique()
    )

    with col3:
        batting_position = st.selectbox(
            "Position",
            ["All"] + batting_positions,
            index=0,
            key="batting_position",
        )

    with col4:
        min_pa = st.number_input(
            "Minimum PA",
            min_value=0,
            max_value=int(batting["pa"].max()),
            value=50,
            step=10,
            key="min_pa",
        )

    filtered_batting = batting[
        batting["season"] == batting_season
    ]

    if batting_level != "All":
        filtered_batting = filtered_batting[
            filtered_batting["level"] == batting_level
        ]

    if batting_position != "All":
        filtered_batting = filtered_batting[
            filtered_batting["position"] == batting_position
        ]

    filtered_batting = filtered_batting[
        filtered_batting["pa"] >= min_pa
    ]

    batting_frame = st.dataframe(
        filtered_batting, 
        column_config={
            "player_id": None,
            "player_name": "Player Name",
            "team_id": None,
            "team_name": "Team Name",
            "season": "Season",
            "league": "League",
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
    st.subheader("Pitching")

    col1, col2, col3= st.columns(3)

    pitching_seasons = sorted(
        pitching["season"].dropna().unique(),
        reverse=True,
    )

    with col1:
        pitching_season = st.selectbox(
            "Season",
            pitching_seasons,
            index=(
                pitching_seasons.index(2026)
                if 2026 in pitching_seasons
                else 0
            ),
            key="pitching_season",
        )

    pitching_levels = sorted(
        pitching["level"].dropna().unique()
    )

    with col2:
        pitching_level = st.selectbox(
            "Level",
            ["All"] + pitching_levels,
            index=0,
            key="pitching_level",
        )

    with col3:
        min_ip = st.number_input(
            "Minimum IP",
            min_value=0.0,
            max_value=float(pitching["ip_decimal"].max()),
            value=30.0,
            step=1.0,
            key="min_ip",
        )

    filtered_pitching = pitching[
        pitching["season"] == pitching_season
    ]

    if pitching_level != "All":
        filtered_pitching = filtered_pitching[
            filtered_pitching["level"] == pitching_level
        ]

    filtered_pitching = filtered_pitching[
        filtered_pitching["ip_decimal"] >= min_ip
    ]

    pitching_frame = st.dataframe(
            filtered_pitching, 
            column_config={
                "player_id": None,
                "player_name": "Player Name",
                "team_id": None,
                "team_name": "Team Name",
                "season": "Season",
                "league": "League",
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
                "strikeout_walk_ratio": st.column_config.NumberColumn( "K/BB", format="%.2f", ),
                "saves": "SV",
                "holds": None,
                "ip_decimal": None,
                "hr_per_9": st.column_config.NumberColumn( "HR/9", format="%.2f", ),
            },
            use_container_width=True,
            hide_index=True
        )
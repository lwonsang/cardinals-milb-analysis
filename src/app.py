import streamlit as st
from components.batting_data import get_seasonal_batting_data, get_level_batting_data, get_positional_batting_data, get_all_batting_data, get_hitting_development_data, get_top_hitters, get_basic_batting_column_config, get_top_hitters_column_config
from components.pitching_data import get_seasonal_pitching_data, get_level_pitching_data, get_all_pitching_data, get_pitching_development_data, get_top_pitchers, get_basic_pitching_column_config, get_top_pitchers_column_config

st.set_page_config(
    page_title="Cardinals Player Development",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

st.title("St. Louis Cardinals Minor League Organization View")

hitters_tab, pitchers_tab = st.tabs(
    ["Hitters", "Pitchers"]
)

def go_to_player_profile(player_id): 
    st.session_state["selected_player_id"] = int(player_id) 
    st.switch_page("pages/player_profile.py")

with hitters_tab:
    st.subheader("Cardinals MiLB Hitter Development View")

    col1, col2, col3, col4 = st.columns(4)

    batting = get_all_batting_data()

    batting_seasons = get_seasonal_batting_data()

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

    batting_levels = get_level_batting_data()

    with col2:
        batting_level = st.selectbox(
            "Level",
            ["All"] + batting_levels,
            index=0,
            key="batting_level",
        )

    batting_positions = get_positional_batting_data()

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

    if not filtered_batting.empty:
        player_options = ( 
            filtered_batting[ 
                ["player_id", "player_name"] 
            ] 
            .drop_duplicates() 
            .sort_values("player_name") 
        ) 
        
        selected_player_name = st.selectbox( 
            "Select a player to view their development profile", 
            player_options["player_name"].tolist(), 
            key="selected_hitter", 
        ) 
        
        selected_player_id = player_options.loc[ 
            player_options["player_name"] == selected_player_name, 
            "player_id", 
        ].iloc[0] 
        
        if st.button(
            "View Player Profile →", 
            key="view_hitter_profile", 
        ): 
            go_to_player_profile(selected_player_id) 
    else:
        st.info("No players match the selected filters.")

    hitting_development = get_hitting_development_data()

    st.markdown("### Hitters to Keep an Eye on")
    st.caption("Find hitters outperforming level and age baselines.") 

    hitter_board = get_top_hitters(
        batting_season,
        batting_level,
        batting_position,
        min_pa,
    )

    display_columns = [
        "player_id",
        "player_name",
        "season",
        "age",
        "position",
        "level",
        "pa",
        "ops",
        "ops_vs_level",
        "ops_vs_age_level",
    ]

    display_columns = [
        col for col in display_columns
        if col in hitter_board.columns
    ]

    top_hitters_column_config = get_top_hitters_column_config()

    st.dataframe(
        hitter_board[display_columns],
        column_config=top_hitters_column_config,
        hide_index=True,
        use_container_width=True,
    )

    basic_hitters_column_config = get_basic_batting_column_config()

    st.markdown("### Full Cardinals MiLB Batting Stats")
    batting_frame = st.dataframe(
        filtered_batting, 
        column_config=basic_hitters_column_config,
        use_container_width=True,
        hide_index=True
    )

with pitchers_tab:
    st.subheader("Cardinals MiLB Pitcher Development View")

    pitching = get_all_pitching_data()

    col1, col2, col3= st.columns(3)

    pitching_seasons = get_seasonal_pitching_data()

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

    pitching_levels = get_level_pitching_data()

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

    if not filtered_pitching.empty:
        player_options = ( 
            filtered_pitching[ 
                ["player_id", "player_name"] 
            ] 
            .drop_duplicates() 
            .sort_values("player_name") 
        ) 
        
        selected_player_name = st.selectbox( 
            "Select a player to view their development profile", 
            player_options["player_name"].tolist(), 
            key="selected_pitcher", 
        ) 
        
        selected_player_id = player_options.loc[ 
            player_options["player_name"] == selected_player_name, 
            "player_id", 
        ].iloc[0] 
        
        if st.button(
            "View Player Profile →", 
            key="view_pitcher_profile", 
        ): 
            go_to_player_profile(selected_player_id) 
    else:
        st.info("No players match the selected filters.")

    pitching_development = get_pitching_development_data()

    st.markdown("### Pitchers to Keep an Eye on") 
    st.caption("Find pitchers outperforming level and age baselines.") 

    pitcher_board = get_top_pitchers(
        pitching_season,
        pitching_level,
        min_ip,
    )

    display_columns = [
        "player_id",
        "player_name",
        "season",
        "age",
        "level",
        "innings_pitched",
        "era",
        "era_vs_level",
        "era_vs_age_level",
    ]

    display_columns = [
        col for col in display_columns
        if col in pitcher_board.columns
    ]

    st.dataframe(
        pitcher_board[display_columns],
        column_config=get_top_pitchers_column_config(),
        hide_index=True,
        use_container_width=True,
    )

    st.markdown("### Full Cardinals MiLB Pitching Stats")
    pitching_frame = st.dataframe(
        filtered_pitching, 
        column_config=get_basic_pitching_column_config(),
        use_container_width=True,
        hide_index=True
    )
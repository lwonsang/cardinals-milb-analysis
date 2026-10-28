import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from processing.config import LEVEL_ORDER
from components.status_data import get_status_data
from components.batting_data import get_all_batting_data, get_hitting_development_data, get_basic_batting_column_config, get_hitter_baseline_comparison_column_config
from components.pitching_data import get_all_pitching_data, get_pitching_development_data, get_basic_pitching_column_config, get_pitcher_baseline_comparison_column_config

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

status = get_status_data()

hitters_tab, pitchers_tab = st.tabs(
    ["Hitters", "Pitchers"]
)

player_id = st.session_state.get("selected_player_id")

if st.button("← Back to Dashboard"):
    st.switch_page("app.py")

with hitters_tab:
    st.subheader("Cardinals MiLB Hitters")

    batting = get_all_batting_data()
    hitting_development = get_hitting_development_data()

    player_names = sorted(
        batting["player_name"].dropna().unique()
    )

    if player_id is not None:
        player_id = int(player_id)
        matching_players = batting[
            batting["player_id"] == player_id
        ]

        if not matching_players.empty:
            selected_player = matching_players["player_name"].iloc[0]
            selected_index = player_names.index(selected_player)
        else:
            selected_index = 0
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

    hitting_comparison = hitting_development[
        hitting_development["player_name"] == selected_player
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
        column_config=get_basic_batting_column_config(),
        use_container_width=True,
        hide_index=True
    )

    st.text(
        "MiLB Hitter Baseline Comparison Stats (per Age/Level):"
    )

    comparison_frame = st.dataframe(
        hitting_comparison, 
        column_config=get_hitter_baseline_comparison_column_config(),
        use_container_width=True,
        hide_index=True
    )

    chart_df = hitting_comparison.copy().sort_values(["season", "level"]).copy()
    chart_df["season_level"] = chart_df["season"].astype(str) + " " + chart_df["level"].astype(str)

    pa = chart_df["plate_appearances"].fillna(0).clip(lower=0)
    if pa.max() == pa.min():
        chart_df["dot_size"] = 12
    else:
        chart_df["dot_size"] = 8 + (
            (pa - pa.min()) / (pa.max() - pa.min())
        ) * 20

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_df["season_level"],
            y=chart_df["ops"],
            mode="lines+markers",
            name="Player OPS",
            marker=dict(
                size=chart_df["dot_size"],
                sizemode="diameter",
                sizemin=8,
                line=dict(width=1, color="white"),
            ),
            customdata=chart_df[["plate_appearances"]],
            hovertemplate=(
                "Season/Level: %{x}<br>"
                "OPS: %{y:.3f}<br>"
                "PA: %{customdata[0]:.0f}"
                "<extra>Player OPS</extra>"
            ),
        ))

    fig.add_trace(
        go.Scatter(
            x=chart_df["season_level"],
            y=chart_df["level_ops"],
            mode="lines+markers",
            name="Level Average OPS",
            marker=dict(size=7),
            line=dict(dash="dot"),
            hovertemplate=(
                "OPS: %{y:.3f}<br>"
            ),
        ))

    fig.add_trace(
        go.Scatter(
            x=chart_df["season_level"],
            y=chart_df["age_level_ops"],
            mode="lines+markers",
            name="Age Level Average OPS",
            marker=dict(size=7),
            line=dict(dash="dash"),
            hovertemplate=(
                "OPS: %{y:.3f}<br>"
            ),
        ))

    fig.update_layout(
        title=f"{chart_df['player_name'].iloc[0]} — OPS Development",
        xaxis_title="Season / Level",
        yaxis_title="OPS",
        hovermode="x unified",
        legend_title="Comparison",
    )

    fig.update_xaxes(type="category")
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))

    st.plotly_chart(fig, use_container_width=True)

with pitchers_tab:
    st.subheader("Cardinals MiLB Pitchers")

    pitching = get_all_pitching_data()
    pitching_development = get_pitching_development_data()

    player_names = sorted(
        pitching["player_name"].dropna().unique()
    )

    if player_id is not None:
        player_id = int(player_id)
        matching_players = pitching[
            pitching["player_id"] == player_id
        ]

        if not matching_players.empty:
            selected_player = matching_players["player_name"].iloc[0]
            selected_index = player_names.index(selected_player)
        else:
            selected_index = 0
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

    pitching_comparison = pitching_development[
        pitching_development["player_name"] == selected_player
    ].sort_values(
        ["season", "level"]
    )

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
        column_config=get_basic_pitching_column_config(),
        use_container_width=True,
        hide_index=True
    )

    st.text(
        "MiLB Pitcher Baseline Comparison Stats (per Age/Level):"
    )

    comparison_frame = st.dataframe(
        pitching_comparison, 
        column_config=get_pitcher_baseline_comparison_column_config(),
        use_container_width=True,
        hide_index=True
    )

    chart_df = pitching_comparison.copy().sort_values(["season", "level"]).copy()
    chart_df["season_level"] = chart_df["season"].astype(str) + " " + chart_df["level"].astype(str)
    
    ip = chart_df["ip_decimal"].fillna(0).clip(lower=0)

    if ip.max() == ip.min():
        chart_df["dot_size"] = 12
    else:
        chart_df["dot_size"] = 8 + (
            (ip - ip.min()) / (ip.max() - ip.min())
        ) * 20

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_df["season_level"],
            y=chart_df["era"],
            mode="lines+markers",
            name="Player ERA",
            marker=dict(
                size=chart_df["dot_size"],
                sizemode="diameter",
                sizemin=8,
                line=dict(width=1, color="white"),
            ),
            customdata=chart_df[["innings_pitched"]],
            hovertemplate=(
                "Season/Level: %{x}<br>"
                "ERA: %{y:.2f}<br>"
                "IP: %{customdata[0]:.1f}"
                "<extra>Player ERA</extra>"
            ),
        ))

    fig.add_trace(
        go.Scatter(
            x=chart_df["season_level"],
            y=chart_df["level_era"],
            mode="lines+markers",
            name="Level Average ERA",
            line=dict(dash="dot"),
            hovertemplate=(
                "ERA: %{y:.2f}<br>"
            ),
        ))

    fig.add_trace(
        go.Scatter(
            x=chart_df["season_level"],
            y=chart_df["age_level_era"],
            mode="lines+markers",
            name="Age Level Average ERA",
            line=dict(dash="dash"),
            hovertemplate=(
                "ERA: %{y:.2f}<br>"
            ),
        ))

    fig.update_layout(
        title=f"{chart_df['player_name'].iloc[0]} — ERA Development",
        xaxis_title="Season / Level",
        yaxis_title="ERA",
        hovermode="x unified",
        legend_title="Comparison",
    )

    fig.update_xaxes(type="category")
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))

    st.plotly_chart(fig, use_container_width=True)
    
 
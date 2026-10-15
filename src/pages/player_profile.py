import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from processing.config import LEVEL_ORDER

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

hitting_development = pd.read_parquet(
    "data/processed/hitting_development.parquet"
)

pitching_development = pd.read_parquet(
    "data/processed/pitching_development.parquet"
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
        "hbp": None,
        "sac_fly": None,
        "sac_bunt": None,
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

    st.text(
        "MiLB Hitter Baseline Comparison Stats (per Age/Level):"
    )

    comparison_frame = st.dataframe(
        hitting_comparison, 
        column_config={
            "player_id": None,
            "player_name": None,
            "team_id": None,
            "team_name": None,
            "season": "Season",
            "league": None,
            "level": "Level",
            "position": None,
            "age": "Age",
            "games": None,
            "plate_appearances": "PA",
            "at_bats": None,
            "hits": None,
            "runs": None,
            "doubles": None,
            "triples": None,
            "home_runs": None,
            "hbp": None,
            "sac_fly": None,
            "sac_bunt": None,
            "walks": None,
            "strikeouts": None,
            "rbi": None,
            "stolen_bases": None,
            "caught_stealing": None,
            "avg": None,
            "obp": None,
            "slg": None,
            "ops": "OPS",
            "babip": None,
            "total_bases": None,
            "pa": None,
            "k_rate": None,
            "bb_rate": None,
            "iso": None,
            "sample_size_category": None,
            "level_players": None,
            "level_plate_appearances": None,
            "level_avg": None,
            "avg_vs_level": None,
            "level_obp": None,
            "obp_vs_level": None,
            "level_slg": None,
            "slg_vs_level": None,
            "level_ops": st.column_config.NumberColumn( "Level OPS", format="%.3f", ),
            "ops_vs_level": st.column_config.NumberColumn( "OPS vs Level", format="%.3f", ),
            "level_k_rate": None,
            "k_rate_vs_level": None,
            "level_bb_rate": None,
            "bb_rate_vs_level": None,
            "level_iso": None,
            "iso_vs_level": None,
            "age_level_players": None,
            "age_level_plate_appearances": None,
            "age_level_avg": None,
            "avg_vs_age_level": None,
            "age_level_obp": None,
            "obp_vs_age_level": None,
            "age_level_slg": None,
            "slg_vs_age_level": None,
            "age_level_ops": st.column_config.NumberColumn( "Age Level OPS", format="%.3f", ),
            "ops_vs_age_level": st.column_config.NumberColumn( "OPS vs Age Level", format="%.3f", ),
            "age_level_k_rate": None,
            "k_rate_vs_age_level": None,
            "age_level_bb_rate": None,
            "bb_rate_vs_age_level": None,
            "age_level_iso": None,
            "iso_vs_age_level": None,
        },
        use_container_width=True,
        hide_index=True
    )

    chart_df = hitting_comparison.copy().sort_values(["season", "level"]).copy()
    chart_df["season_level"] = chart_df["season"].astype(str) + " " + chart_df["level"].astype(str)
    chart_df["level"] = pd.Categorical(
        chart_df["level"],
        categories = LEVEL_ORDER,
        ordered = True
    )
    chart_df = chart_df.sort_values(["season", "level"])

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
        column_config={
            "player_id": None,
            "player_name": None,
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

    st.text(
        "MiLB Pitcher Baseline Comparison Stats (per Age/Level):"
    )

    comparison_frame = st.dataframe(
        pitching_comparison, 
        column_config={
            "player_id": None,
            "player_name": None,
            "team_id": None,
            "team_name": None,
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
            "whip": None,
            "strikeouts_per_9": None,
            "walks_per_9": None,
            "hits_per_9": None,
            "hr_per_9": None,
            "strikeout_walk_ratio": st.column_config.NumberColumn( "K/BB", format="%.2f", ),
            "saves": None,
            "holds": None,
            "ip_decimal": None,
            "level_players": None,
            "level_innings_pitched": None,
            "level_era": st.column_config.NumberColumn( "Level ERA", format="%.2f", ),
            "level_whip": None,
            "level_strikeouts_per_9": None,
            "level_walks_per_9": None,
            "level_hits_per_9": None,
            "level_hr_per_9": None,
            "level_strikeout_walk_ratio": st.column_config.NumberColumn( "Level K/BB", format="%.2f", ),
            "age_level_players": None,
            "age_level_innings_pitched": None,
            "age_level_era": st.column_config.NumberColumn( "Age Level ERA", format="%.2f", ),
            "age_level_whip": None,
            "age_level_strikeouts_per_9": None,
            "age_level_walks_per_9": None,
            "age_level_hits_per_9": None,
            "age_level_hr_per_9": None,
            "age_level_strikeout_walk_ratio": st.column_config.NumberColumn( "Age Level K/BB", format="%.2f", ),
            "era_vs_level": st.column_config.NumberColumn( "ERA vs Level", format="%.2f", ),
            "whip_vs_level": None,
            "strikeouts_per_9_vs_level": None,
            "hits_per_9_vs_level": None,
            "walks_per_9_vs_level": None,
            "hr_per_9_vs_level": None,
            "strikeout_walk_ratio_vs_level": None,
            "era_vs_age_level": None,
            "whip_vs_age_level": None,
            "strikeouts_per_9_vs_age_level": None,
            "walks_per_9_vs_age_level": None,
            "hits_per_9_vs_age_level": None,
            "hr_per_9_vs_age_level": None,
            "strikeout_walk_ratio_vs_age_level": st.column_config.NumberColumn( "K/BB vs Age Level", format="%.2f", ),
        },
        use_container_width=True,
        hide_index=True
    )

    chart_df = pitching_comparison.copy().sort_values(["season", "level"]).copy()
    chart_df["season_level"] = chart_df["season"].astype(str) + " " + chart_df["level"].astype(str)
    chart_df["level"] = pd.Categorical(
        chart_df["level"],
        categories = LEVEL_ORDER,
        ordered = True
    )
    chart_df = chart_df.sort_values(["season", "level"])
    
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
    
 
# Cardinals Minor League Player Development Dashboard

An interactive baseball analytics dashboard for exploring player performance and development across the St. Louis Cardinals' minor league system. combining multi-season Minor League batting and pitching stats with organizational roster status information to help explore prospect performance and development in context compared to level-wide and age-based baseline stats. The goal is to make it easier to evaluate player performance in context, explore trends across seasons and levels, and identify players whose statistical production stands out relative to their peers.



**Features:**

-Active Player Organization View that shows minor league batting and pitching statistics by season and level for all active Cardinals minor league players. Players can be filtered by level, position, season, and minimum plate appearances/innings pitched. Core performance metrics, including HR, batting average, OBP, SLG, OPS, SB, K%, BB%, and ISO for hitters and ERA, WHIP, K/9, BB/9, H/9, K/BB, and HR/9 for pitchers, are shown here.

-Players to Keep an Eye on, a spotlight table showing players who have been outperforming their level and age baselines by a good amount (with PA/IP above minimum standards).

-A player development view to show performance across minor league levels and seasons for each Cardinals active minor league player with their development over time compared to their peers. The main purpose of these profiles are to explore changes in performances as players progress through the Cardinals minor league system. Includes performance visualization charts through Plotly to visually show players' development over time compared to baseline age and level-wide standards (OPS/ERA)



**Tech Stack:**

Uses Python, pandas, Streamlit, Plotly, Parquet, and most importantly, the MLB Stats API.



**Access instructions:**

https://lwonsang-cardinals-milb-analysis-srcapp-ykkukn.streamlit.app/

Or to run locally:
After cloning this repository, create and activate a virtual environment:
python -m venv .venv

Install dependencies:
pip install -r requirements.txt

Run data pipelines:
python -m src.pipeliens.build_dataset

Run dashboard:
streamlit run app.py



**Future Plans:**

-Add additional development indicators such as rolling performance, recent performance trends, and Statcast data
-Expand visual comparisons across seasons and level
-Continue developing player spotlight table

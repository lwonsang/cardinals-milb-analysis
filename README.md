# cardinals-milb-analysis

Cardinals MiLB Player Developmental Dashboard using MLB Stats API data, combining multi-season Minor League batting and pitching stats with organizational roster status information to help explore prospect performance compared to their current level.

Access instructions:
git clone https://github.com/lwonsang/cardinals-milb-analysis.git

cd cardinals-milb-analysis

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

streamlit run src/app.py

Future Plans:
-Create a player development view (for top prospects) with level progression, season-by-season performance, comparison to peers (in the same age bracket and level) and development indicators (including Statcast data) to help learn about promotion readiness and future potential.

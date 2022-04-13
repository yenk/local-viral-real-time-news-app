# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc # for interactive interaces dropsdowns, filters, graphs
import dash_bootstrap_components as dbc
import dash_html_components as html # access html tags
import plotly.express as px
import pandas as pd
from server import * 

# print()

# Instantiate dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY] ) 

# Define the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# app = Dash(__name__)
df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv")

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)

app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])

# Run flask app
if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8050)

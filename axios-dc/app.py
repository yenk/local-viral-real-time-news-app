from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

avg_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-counties-2022.csv")
avg_data = avg_data[avg_data["county"] == "District of Columbia"]
avg_data = avg_data.to_csv('covdc.csv')

data = pd.read_csv("covdc.csv")
data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
data.sort_values("date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Live Covid Daily Updates in DC!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Average Daily Covid Stats in DC", className="header-title"
                ),
                html.P(
                    children="Covid data is fetched daily when it's available & at end of the day!"
                    " https://github.com/nytimes/covid-19-data "
                    " https://github.com/yenk/local-viral-dash",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                dcc.DatePickerRange(
                    id="date-range",
                    min_date_allowed=data.date.min().date(),
                    max_date_allowed=data.date.max().date(),
                    start_date=data.date.min().date(),
                    end_date=data.date.max().date(),
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="covid-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="deaths-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),

        #### new
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="covid_100k-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="deaths_100k-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        ### ends
    ]
)


@app.callback(
    [Output("covid-chart", "figure"), Output("deaths-chart", "figure"), 
        Output("covid_100k-chart", "figure"), Output("deaths_100k-chart", "figure")],
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(start_date, end_date):
    mask = (
        (data.date >= start_date)
        & (data.date <= end_date)
    )
    filtered_data = data.loc[mask, :]

    covid_chart_figure = {  
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["cases_avg"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Average Daily Covid Cases", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#9acd32"],
        },
    }

    deaths_chart_figure = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["deaths_avg"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Average Daily Confirmed Covid Deaths", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#ff0000"],
        },
    }

    ### starts
    covid_100k_chart_figure = {  
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["cases_avg_per_100k"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Average Daily Covid Cases/100k", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#6e57d2"],
        },
    }

    deaths_100k_chart_figure = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["deaths_avg_per_100k"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Average Daily Confirmed Covid Deaths/100k", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#db6204"],
        },
    }

    ### ends

    return covid_chart_figure, deaths_chart_figure, covid_100k_chart_figure, deaths_100k_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)

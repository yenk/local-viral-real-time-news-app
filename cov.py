import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

data = pd.read_csv("local_avg_covid_data.csv")
data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
data.sort_values("date", inplace=True)

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Average Daily Covid Cases in DC",),
        html.P(
            children="DC's daily average Covid cases"
            "and deaths beginning January 2022 to current date",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["date"],
                        "y": data["cases_avg_per_100k"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Daily Covid Cases in DC"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["date"],
                        "y": data["deaths_avg"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Daily Covid Deaths in DC"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
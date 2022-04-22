from flask import render_template
from backend import server


def fetch_page():
    dash_content = server.get_dash_content(
        "Washington DC", ["Things to Do", "Food and Drink"]
    )
    events = server.get_local_event_data("20001", 75)
    weather = server.get_local_weather_data("20001")
    bus_data = server.get_bus_alert_data()
    metro_data = server.get_metro_alert_data()
    covid_cases = server.get_current_day_covid_cases("District of Columbia")
    covid_week_avg = server.get_week_avg_covid_cases("District of Columbia")
    return render_template(
        "hack.html",
        dash_content=dash_content,
        events=events["events"],
        weather=weather,
        bus_data=bus_data,
        metro_data=metro_data,
        covid_cases=covid_cases,
        covid_week_avg=covid_week_avg,
    )

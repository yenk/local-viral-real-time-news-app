from flask import Flask, render_template
from backend import server
from dashy import cov
# import server 
# import cov 

app = Flask(__name__)

@app.route("/")
def index():
    dash_content = server.get_dash_content(
        "Washington DC", ["Things to Do", "Food and Drink"]
    )
    events = server.get_local_event_data("20001", 50)
    weather = server.get_local_weather_data("20001")
    bus_data = server.get_bus_alert_data()
    metro_data = server.get_metro_alert_data()
    return render_template(
        "hack.html",
        dash_content=dash_content,
        events=events["events"],
        weather=weather,
        bus_data=bus_data,
        metro_data=metro_data,
    )


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template
from backend import server

app = Flask(__name__)


@app.route("/")
def index():
    dash_content = server.get_dash_content(
        "Washington DC", ["Things to Do", "Food and Drink"]
    )
    events = server.get_local_event_data("20001", 50)
    return render_template(
        "hack.html",
        dash_content=dash_content,
        events=events["events"],
    )


if __name__ == "__main__":
    app.run(debug=True)

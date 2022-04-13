from flask import Flask, render_template
from backend import server

app = Flask(__name__)


@app.route("/")
def index():
    dash_content = server.get_dash_content(
        "Washington DC", ["Things to Do", "Food and Drink"]
    )
    return render_template("hack.html", dash_content=dash_content)


if __name__ == "__main__":
    app.run(debug=True)

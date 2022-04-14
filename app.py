from flask import Flask
from web import webapp


app = Flask(__name__, template_folder="web/templates", static_folder="web/static")


@app.route("/")
def index():
    return webapp.fetch_page()


if __name__ == "__main__":
    app.run(debug=True)

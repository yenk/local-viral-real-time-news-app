from flask import Flask, render_template
from web import webapp 


app = Flask(__name__)

@app.route("/")
def index():
    return webapp.fetch_page()



if __name__ == "__main__":
    app.run(debug=True)

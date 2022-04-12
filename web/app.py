from flask import Flask, render_template
from dash import Dash, html

app = Flask(__name__)
myDashBoard = html.Div([
    html.H1('Hello Dash'),
    html.Div([
        html.P('Dash converts Python classes into HTML'),
        html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
    ])
])

@app.route('/test')
def index():
  return render_template('hack.html', myDashBoard)

if __name__ == '__main__':
  app.run(debug=True)
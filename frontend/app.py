import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does
from whitenoise import WhiteNoise   #for serving static files on Heroku

# Instantiate dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY] ) 

# Define the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Your app title" #browser tab
    
    # Header
    header = html.Div([html.Br(), dcc.Markdown(""" # Welcome to Axios Best and Foremost DC's Local News! """), html.Br()])
    
    # Body 
    body = html.Div([dcc.Markdown(""" See What's Happening in DC! """), html.Br(), html.Img(src='dc_heading.png')])

    # Footer
    footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built at ![Image](logo.png) with ![Image](heart.png) using [Dash](https://plotly.com/dash/) and [Heroku](https://devcenter.heroku.com/) """)])
    
    # Assemble dash layout 
    app.layout = html.Div([header, body, footer])

    return app

# Construct the dash layout
create_dash_layout(app)

# Run flask app
if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8050)























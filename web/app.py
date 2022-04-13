from flask import Flask, render_template, redirect, url_for, request, flash
import server 

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('hack.html', me="lizna")

if __name__ == '__main__':
  app.run(debug=True)
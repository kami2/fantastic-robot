from flask import render_template
from smallworker import app


@app.route("/hello")
def hello():
    return "Hello World"


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results

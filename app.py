from flask import Flask, render_template
app = Flask(__name__)


@app.route("/hello")
def hello():
    return "Hello World"


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


if __name__ == "__main__":
    app.run()

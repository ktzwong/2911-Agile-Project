from flask import Flask, render_template, redirect, url_for
from pathlib import Path

app = Flask(__name__)
app.instance_path = Path(" ").resolve()




@app.route("/")
def home():
    return render_template("home.html")




if __name__ == "__main__":
     app.run(debug=True, port=8888)
from flask import Flask, request, jsonify, render_template

app = Flask(_name_)

@app.route("/")
def home():
    return render_template("index.html")

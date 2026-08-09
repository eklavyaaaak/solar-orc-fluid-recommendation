from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()

    solar = float(data.get("solar", 0))
    temperature = float(data.get("temperature", 25))

    if solar >= 800 and temperature >= 30:
        fluid = "Toluene"
    elif solar >= 500:
        fluid = "R245fa"
    else:
        fluid = "R134a"

    return jsonify({
        "recommended_fluid": fluid,
        "solar_radiation": solar,
        "temperature": temperature
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0",
port=5000)

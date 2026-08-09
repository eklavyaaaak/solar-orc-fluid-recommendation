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

    # Working-fluid recommendation
    if solar >= 800 and temperature >= 30:
        fluid = "Toluene"
    elif solar >= 500:
        fluid = "R245fa"
    else:
        fluid = "R134a"

    # Basic ORC estimation
    heat_absorption_rate = max(0, solar * 0.70)

    net_power_output = heat_absorption_rate * 0.12

    system_efficiency = (
        (net_power_output / heat_absorption_rate) * 100
        if heat_absorption_rate > 0
        else 0
    )

    # Approximate pressures for demonstration
    evaporator_pressure = max(1, temperature * 0.08)

    condenser_pressure = max(0.5, 30 * 0.03)

    return jsonify({
        "recommended_fluid": fluid,
        "recommended_working_fluid": fluid,
        "solar_radiation": solar,
        "temperature": temperature,
        "heat_absorption_rate": round(heat_absorption_rate, 2),
        "net_power_output": round(net_power_output, 2),
        "system_efficiency": round(system_efficiency, 2),
        "evaporator_pressure": round(evaporator_pressure, 2),
        "condenser_pressure": round(condenser_pressure, 2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

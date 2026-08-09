from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# ORC Simulation
# -----------------------------
@app.route("/simulate", methods=["POST"])
def simulate():

    try:
        # Get data sent from index.html
        data = request.get_json()

        solar = float(data.get("solarIrradiance", 0))
        collector_area = float(data.get("collectorArea", 0))
        collector_efficiency = float(
            data.get("collectorEfficiency", 0)
        )
        ambient_temperature = float(
            data.get("ambientTemperature", 25)
        )
        selected_fluid = data.get("workingFluid", "Auto")


        # -----------------------------
        # Input Validation
        # -----------------------------
        if solar <= 0:
            return jsonify({
                "error": "Solar irradiance must be greater than 0."
            }), 400

        if collector_area <= 0:
            return jsonify({
                "error": "Collector area must be greater than 0."
            }), 400

        if collector_efficiency <= 0 or collector_efficiency > 100:
            return jsonify({
                "error": "Collector efficiency must be between 1 and 100%."
            }), 400


        # -----------------------------
        # Solar Heat Absorption
        # -----------------------------
        solar_power = solar * collector_area

        heat_absorption = (
            solar_power * collector_efficiency / 100
        )

        # W → kW
        heat_absorption_kw = heat_absorption / 1000


        # -----------------------------
        # Working Fluid Selection
        # -----------------------------
        if selected_fluid == "Auto":

            if solar >= 800 and ambient_temperature >= 30:
                fluid = "R245fa"

            elif solar >= 500:
                fluid = "R134a"

            elif solar >= 300:
                fluid = "R123"

            else:
                fluid = "Isobutane"

        else:
            fluid = selected_fluid


        # -----------------------------
        # ORC Efficiency
        # -----------------------------
        efficiency_values = {
            "R245fa": 14.0,
            "R134a": 12.0,
            "R123": 15.0,
            "Isobutane": 13.0
        }

        system_efficiency = efficiency_values.get(
            fluid,
            12.0
        )


        # -----------------------------
        # Net Power Output
        # -----------------------------
        net_power_output = (
            heat_absorption_kw *
            system_efficiency /
            100
        )


        # -----------------------------
        # Evaporator Pressure
        # -----------------------------
        evaporator_pressures = {
            "R245fa": 15.0,
            "R134a": 12.0,
            "R123": 10.0,
            "Isobutane": 20.0
        }

        evaporator_pressure = evaporator_pressures.get(
            fluid,
            10.0
        )


        # -----------------------------
        # Condenser Pressure
        # -----------------------------
        condenser_pressures = {
            "R245fa": 2.0,
            "R134a": 3.0,
            "R123": 1.5,
            "Isobutane": 4.0
        }

        condenser_pressure = condenser_pressures.get(
            fluid,
            2.0
        )


        # -----------------------------
        # Send Results to Website
        # -----------------------------
        return jsonify({

            "optimalWorkingFluid": fluid,

            "heatAbsorptionRate": round(
                heat_absorption_kw,
                3
            ),

            "netPowerOutput": round(
                net_power_output,
                3
            ),

            "systemEfficiency": round(
                system_efficiency,
                2
            ),

            "evaporatorPressure": round(
                evaporator_pressure,
                2
            ),

            "condenserPressure": round(
                condenser_pressure,
                2
            )
        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# Run Flask Application
# -----------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )

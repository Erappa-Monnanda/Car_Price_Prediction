from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# ✅ Define homepage route
@app.route('/')
def home():
    return render_template("index.html")

# ✅ Define prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("Received form data:", request.form)  # ✅ Debugging
        
        # ✅ Get input values from form
        year = request.form.get('Year')
        brand = request.form.get('Brand')
        mileage = request.form.get('Mileage')
        engine_size = request.form.get('Engine_Size')
        fuel_type = request.form.get('Fuel_Type')
        transmission = request.form.get('Transmission')

        # ✅ Ensure no empty values
        if None in [year, brand, mileage, engine_size, fuel_type, transmission]:
            return jsonify({"error": "Missing input values!"}), 400
        
        # ✅ Convert values to correct types
        year = int(year)
        mileage = float(mileage)
        engine_size = float(engine_size)

        # ✅ Create DataFrame for prediction
        input_data = pd.DataFrame([[year, brand, mileage, engine_size, fuel_type, transmission]],
                                  columns=['Year', 'Brand', 'Mileage', 'Engine_Size', 'Fuel_Type', 'Transmission'])

        # ✅ Make prediction
        prediction = model.predict(input_data)[0]

        return render_template("index.html", prediction_text=f"Predicted Car Price: ${prediction:,.2f}")

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ✅ Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

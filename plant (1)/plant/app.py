from flask import Flask, render_template, request
import pandas as pd
import pickle

# Load the pre-trained model
with open('dcl_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('en_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Initialize Flask app
app = Flask(__name__)

# Define the input features for the plant disease prediction model
input_columns = [
    'Soil_Moisture', 'Ambient_Temperature', 'Soil_Temperature', 'Humidity',
    'Light_Intensity', 'Soil_pH', 'Nitrogen_Level', 'Phosphorus_Level',
    'Potassium_Level', 'Chlorophyll_Content', 'Electrochemical_Signal'
]

# Route to display the form and handle user input
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Extract the user input data
        user_input = {
            'Soil_Moisture': float(request.form['Soil_Moisture']),
            'Ambient_Temperature': float(request.form['Ambient_Temperature']),
            'Soil_Temperature': float(request.form['Soil_Temperature']),
            'Humidity': float(request.form['Humidity']),
            'Light_Intensity': float(request.form['Light_Intensity']),
            'Soil_pH': float(request.form['Soil_pH']),
            'Nitrogen_Level': float(request.form['Nitrogen_Level']),
            'Phosphorus_Level': float(request.form['Phosphorus_Level']),
            'Potassium_Level': float(request.form['Potassium_Level']),
            'Chlorophyll_Content': float(request.form['Chlorophyll_Content']),
            'Electrochemical_Signal': float(request.form['Electrochemical_Signal'])
        }
        
        # Convert user input into a DataFrame
        input_df = pd.DataFrame([user_input])

        # Make prediction without scaling
        prediction = model.predict(input_df[input_columns])

        # Map the prediction to the plant health status
        plant_health_status = {
            0: 'Healthy',
            1: 'moderate stress',
            2: 'High stress',
        }
        diagnosis = plant_health_status[prediction[0]]

        # Display prediction result
        return render_template('result.html', diagnosis=diagnosis)

    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

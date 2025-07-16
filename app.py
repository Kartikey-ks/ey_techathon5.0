from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('C:\\Users\\lenovo\\project\\backend\\model\\predictive_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Get the login data
    name = request.form.get('name')
    age = request.form.get('age')
    address = request.form.get('address')
    
    # Debugging: print the received data
    print(f"Received login data: Name={name}, Age={age}, Address={address}")

    # Ensure all fields are received
    if not name or not age or not address:
        return jsonify({'error': 'Missing fields'}), 400

    # After login, pass user data to the template and show prediction form
    return render_template('index.html', name=name, age=age, address=address)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Debugging: Check what data is being received
        print("Received data for prediction:", request.form)

        # Extract data from the form
        age = request.form.get('age')
        hypertension = request.form.get('hypertension')
        heart_disease = request.form.get('heart_disease')
        avg_glucose_level = request.form.get('avg_glucose_level')
        bmi = request.form.get('bmi')

        # Validate the data
        if not age or not hypertension or not heart_disease or not avg_glucose_level or not bmi:
            return jsonify({'error': 'Missing fields for prediction'}), 400

        # Convert data to appropriate types
        age = int(age)
        hypertension = int(hypertension)
        heart_disease = int(heart_disease)
        avg_glucose_level = float(avg_glucose_level)
        bmi = float(bmi)

        # Create a DataFrame for model input
        data = pd.DataFrame([{
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'avg_glucose_level': avg_glucose_level,
            'bmi': bmi
        }])

        # Predict using the model
        prediction = model.predict(data)[0]
        risk_level = "High Risk" if prediction == 1 else "Low Risk"

        # Return prediction result with the user's name and address
        return render_template('index.html', prediction=risk_level, name=request.form['name'], age=request.form['age'], address=request.form['address'])

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

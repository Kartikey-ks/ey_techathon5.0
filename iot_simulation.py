import requests
import random
import time

backend_url = "http://127.0.0.1:5000/predict"

while True:
    # Simulate patient data
    simulated_data = {
        "age": random.randint(20, 90),
        "hypertension": random.randint(0, 1),
        "heart_disease": random.randint(0, 1),
        "avg_glucose_level": random.uniform(70, 200),
        "bmi": random.uniform(15, 35)
    }

    # Send data to the backend for prediction
    response = requests.post(backend_url, json=simulated_data)
    
    # Output the result in a friendly format
    if response.status_code == 200:
        prediction = response.json()
        print(f"Sent data: {simulated_data}, Prediction: {prediction}")
    else:
        print(f"Failed to get prediction. Error: {response.status_code}")

    # Wait before sending the next data
    time.sleep(5)

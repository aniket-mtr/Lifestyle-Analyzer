import sys
import os
import pickle
import numpy as np

def process_input(input_array):
    if len(input_array) != 5:
        raise ValueError("Input array must have exactly 5 elements.")

    # Process inputs
    core_circle = input_array[0] / 10  # Scale 0-10 to 0-1
    bmi = 0 if 18.5 <= input_array[1] <= 24.9 else 1  # Binary encoding for BMI range
    steps = input_array[2] / 10000  # Scale 0-10,000 to 0-1
    sleep = input_array[3] / 10  # Scale 0-10 to 0-1
    wlb = input_array[4] / 10  # Scale 0-10 to 0-1

    # Construct and return processed array
    processed_array = [core_circle, bmi, steps, sleep, wlb]
    return np.array(processed_array)


if __name__ == "__main__":
    # Load the model
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to kmeans_model.pkl
    model_path = os.path.join(script_dir, '../support/kmeans_model.pkl')

    # Load the model
    with open(model_path, 'rb') as file:
        kmeans = pickle.load(file)


    # Get input data from command-line arguments
    input_data = list(map(float, sys.argv[1:]))
    input_array = np.array(input_data)

    #process the input
    input_array=process_input(input_array).reshape(1, -1)

    # Make prediction
    prediction = kmeans.predict(input_array)
    #print(prediction[0])  # Send result back to Node.js
    if prediction == 0:
        print('Active and Socially Balanced') 
    elif prediction == 1:
        print('Health Challenged with Poor Work-Life Balance') 
    else:
        print('Isolated and Sedentary')

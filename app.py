from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    manufacturer = request.form['manufacturer']
    year = int(request.form['year'])
    category = request.form['category']
    interiors = request.form['interiors']
    fuel_type = request.form['fuel_type']
    engine_volume = float(request.form['engine_volume'])
    turbo = eval(request.form['turbo'])
    mileage = int(request.form['mileage'])
    cylinders = int(request.form['cylinders'])
    gear_box = request.form['gear_box']
    drive_wheel  = request.form['drive_wheel']
    door = int(request.form['door'])
    wheel = request.form['wheel']
    color = request.form['color']
    airbags = int(request.form['airbags'])
    levy = float(request.form['levy'])

    with open('encoded_values.pkl', 'rb') as file:
        mapping_dict = pickle.load(file)

    interiors = mapping_dict['interiors'][interiors]
    fuel_type = mapping_dict['fuel_type'][fuel_type]
    gear_box = mapping_dict['gear_box'][gear_box]
    drive_wheel = mapping_dict['drive-wheel'][drive_wheel]
    wheel = mapping_dict['wheel'][wheel]
    category = mapping_dict['category'][category]
    manufacturer = mapping_dict['manufacturer'][manufacturer]
    color = mapping_dict['color'][color]

    input_dict = {
        'levy': levy,
        'manufacturer' : manufacturer,
        'prod._year': year,
        'category': category,
        'leather_interior': interiors,
        'fuel_type': fuel_type,
        'engine_volume':engine_volume,
        'Mileage/km': mileage,
        'cylinders': cylinders,
        'gear_box_type': gear_box,
        'drive_wheels': drive_wheel,
        'doors': door,
        'wheel': wheel,
        'color': color,
        'airbags': airbags,
        'Turbo_engine': turbo
    }
    print(input_dict)

    input_df = pd.DataFrame([input_dict])

    # Convert the DataFrame to a 2D array
    input_array = input_df.values.reshape(1, -1)


    print(input)

    with open('rfModel_CarPricePrediction.pkl', 'rb') as f:
        model = pickle.load(f)

    predictions = model.predict(input_array)
    output = "Price of the car is predicted to be $"+format(predictions[0], ".2f")
    print(output)

    return render_template('output.html', output = output)

if __name__ == '__main__':
    app.run()
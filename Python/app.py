import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/prediction": {"origins": "http://localhost:3000"}})
def prediction(lst):
    filename = 'MLmodel/predictor4.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value[0]  # Return the prediction value, not a list

@app.route('/prediction', methods=['POST'])
def predict():
    try:
        data = request.get_json()

    
        NumberOfBedroom = int(data['NumberOfBedroom'])
        NumberOfBathroom = int(data['NumberOfBathroom'])
        SizeOfLivingArea = int(data['SizeOfLivingArea'])
        SizeOfLandArea = float(data['SizeOfLandArea'])
        NumberOfFloors = float(data['NumberOfFloors'])
        CurrencyRate = int(data['CurrencyRate'])
        Locations = data['Locations']

        Location_List = ['Athurugiriya', 'Battaramulla', 'Malabe', 'Nugegoda', 'Piliyandala', 'Thalawatugoda']

        feature_list = [NumberOfBedroom, NumberOfBathroom, SizeOfLivingArea, SizeOfLandArea, NumberOfFloors, CurrencyRate]

        for item in Location_List:
            if item == Locations:
                feature_list.append(1)
            else:
                feature_list.append(0)

       
        pred_value = prediction(feature_list)
        pred_value = round(pred_value, 2)

       
        response = {
            "prediction": pred_value
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

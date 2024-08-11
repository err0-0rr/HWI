from flask import Flask, jsonify, request 
import json
from sklearn.preprocessing import MinMaxScaler
from llama3 import test
from gemini import gemini_test,parameters_via_city
from river_discharge import get_elevation_river_discharge
import joblib
import numpy as np

app = Flask(__name__) 

model = joblib.load(r"C:\Users\91833\Downloads\linear_regression_HWI_V1.joblib")
scaler = joblib.load(r"C:\Users\91833\Downloads\scaler_HWI_V1.joblib")
default_values = {
    'MonsoonIntensity': 4.921450,
    'TopographyDrainage': 4.926671,
    'RiverManagement': 4.955322,
    'Deforestation': 4.942240,
    'Urbanization': 4.942517,
    'ClimateChange': 4.934093,
    'DamsQuality': 4.955878,
    'Siltation': 4.927791,
    'AgriculturalPractices': 4.942619,
    'Encroachments': 4.949230,
    'IneffectiveDisasterPreparedness': 4.945239,
    'DrainageSystems': 4.946893,
    'CoastalVulnerability': 4.953999,
    'Landslides': 4.931376,
    'Watersheds': 4.929032,
    'DeterioratingInfrastructure': 4.925907,
    'PopulationScore': 4.927520,
    'WetlandLoss': 4.950859,
    'InadequatePlanning': 4.940587,
    'PoliticalFactors': 4.939004
}


weights = {
    'MonsoonIntensity': 0.2,
    'TopographyDrainage': 0.1,
    'RiverManagement': 0.1,
    'Deforestation': 0.05,
    'Urbanization': 0.15,
    'ClimateChange': 0.05,
    'DamsQuality': 0.1,
    'Siltation': 0.05,
    'AgriculturalPractices': 0.05,
    'DrainageSystems': 0.1,
    'CoastalVulnerability': 0.05,
    'Landslides': 0.05,
    'Watersheds': 0.05,
    'DeterioratingInfrastructure': 0.1,
    'PopulationScore': 0.1,
    'WetlandLoss': 0.05,
    'InadequatePlanning': 0.1,
    'PoliticalFactors': 0.05,
    'FloodProbability': 0.3
}
min_severity = 4.1975
max_severity = 12.010000000000002


@app.route('/', methods = ['GET', 'POST']) 
def home(): 
    if(request.method == 'GET'): 
  
        data = "hello world"
        return jsonify({'data': data}) 
  
def classify_severity(normalized_score):
    if normalized_score < 0.25:
        return 0  # Low
    elif normalized_score < 0.5:
        return 1  # Moderate
    elif normalized_score < 0.75:
        return 2  # High
    else:
        return 3  # Very High
    

# @app.route('/llm', methods = ['GET']) 
# def testllm():
#     return test()

@app.route('/river', methods = ['GET']) 
def testrivel():
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    return get_elevation_river_discharge(latitude, longitude)

@app.route('/gemini', methods = ['GET']) 
def gemini_call():
    city = request.args.get('city', type=str)
    return parameters_via_city(city)



@app.route('/predictcondition', methods=['Post'])
def predictcondition():
    data = request.json
    # Ensure all expected parameters are in the input
    input_data = [[data.get(param, default) for param, default in default_values.items()]]
    scaled_new_data = scaler.transform(input_data)
    prediction = model.predict(scaled_new_data)
    flood_probability = prediction[0]
    #severity
    severity = sum(input_data[0][row] * weight for row, weight in enumerate(weights.values()))
    severity+=weights["FloodProbability"]
    normalized_severity = (severity - min_severity) / (max_severity - min_severity)
    severity_scaled = classify_severity(normalized_severity)

    return jsonify({'FloodProbability': flood_probability, 'Severity':severity_scaled})

@app.route('/predict', methods=['Get'])
def predict():
    city = request.args.get('city', type=str)
    
    data=json.loads(parameters_via_city(city))
    # Ensure all expected parameters are in the input
    input_data = [[data.get(param, default) for param, default in default_values.items()]]
    scaled_new_data = scaler.transform(input_data)
    prediction = model.predict(scaled_new_data)
    flood_probability = prediction[0]
    #severity
    severity = sum(input_data[0][row] * weight for row, weight in enumerate(weights.values()))
    severity+=weights["FloodProbability"]
    normalized_severity = (severity - min_severity) / (max_severity - min_severity)
    severity_scaled = classify_severity(normalized_severity)

    return jsonify({'FloodProbability': flood_probability, 'Severity':severity_scaled, 'Conditions':data})



if __name__ == '__main__': 
    app.run(debug = True) 
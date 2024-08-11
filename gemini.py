import os
import google.generativeai as genai
from os import environ



def gemini_test(msg):

    

    # Create the model
    generation_config = {
    # "temperature": 1,
    # "top_p": 0.95,
    # "top_k": 64,
    # "max_output_tokens": 8192,
    # "response_mime_type": "text/plain",
    }

    # model = genai.GenerativeModel(
    # model_name="gemini-1.5-pro",
    # generation_config=generation_config,
    # # safety_settings = Adjust safety settings
    # # See https://ai.google.dev/gemini-api/docs/safety-settings
    # )

    # chat_session = model.start_chat(
    # history=[]
    # )
    genai.configure(api_key="AIzaSyCCVjezpDx9LAPtrlv3VgwhrykBY4xW5p4")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(msg)
    return response.text

def parameters_via_city(city):
    msg= " Given the name of a city name "+str(city)+""", please provide output in JSON format starting with { with numerical values on a scale of 1 to 10 for the following parameters. The values should be based on the city's geolocation and relevant environmental and infrastructure factors. Do not include any explanation of parameters:

'MonsoonIntensity'
'TopographyDrainage'
'RiverManagement'
'Deforestation'
'Urbanization'
'ClimateChange'
'DamsQuality'
'Siltation'
'AgriculturalPractices'
'Encroachments'
'IneffectiveDisasterPreparedness'
'DrainageSystems'
'CoastalVulnerability'
'Landslides'
'Watersheds'
'DeterioratingInfrastructure'
'PopulationScore'
'WetlandLoss'
'InadequatePlanning'
'PoliticalFactors'"""

    genai.configure(api_key="AIzaSyCCVjezpDx9LAPtrlv3VgwhrykBY4xW5p4")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content(msg)
    return response.text


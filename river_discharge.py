from flask import request, jsonify
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def get_elevation_river_discharge(latitude, longitude):
    # Extract latitude and longitude from request arguments

    if latitude is None or longitude is None:
        return jsonify({"error": "Please provide latitude and longitude"}), 400

    # API request parameters
    url = "https://flood-api.open-meteo.com/v1/flood"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "river_discharge",
        "forecast_days":7
    }

    try:
        # Make API request
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Extract elevation and river discharge data
        elevation = response.Elevation()
        daily = response.Daily()
        daily_river_discharge = daily.Variables(0).ValuesAsNumpy()

        # Create a DataFrame for daily river discharge data
        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "river_discharge": daily_river_discharge
        }
        daily_dataframe = pd.DataFrame(data=daily_data)

        # Convert the DataFrame to a JSON-serializable dictionary
        daily_dict = daily_dataframe.to_dict(orient='records')

        # Return the elevation and river discharge data
        return jsonify({
            "latitude": latitude,
            "longitude": longitude,
            "elevation": elevation,
            "river_discharge": daily_dict
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

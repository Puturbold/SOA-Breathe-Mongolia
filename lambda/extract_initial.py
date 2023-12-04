import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
import os


def testAPI():
  api_key = "9203abc1267cb56ec6c9f843271ceef8ce4d3c445923782a5b491296a6f07386"

  # Define the API URL and Header
  api_url = "https://api.openaq.org/v2/measurements"
  headers = {
      "Authorization": f"Bearer {api_key}"
  }
  param = {'parameter': ['pm25'], 'limit': 10000, 'location_id': 525556, 'date_from': '2023-05-23T18:01:00Z', 'date_to': '2023-07-22T18:01:00Z'}
  response = requests.get(api_url, params=params, headers=headers)
  if response.status_code == 200:
    # Convert the response to JSON format
    print("Success!")
  else:
    print(f"Error: Failed to fetch data from the API. Status code: {response.status_code}")

# this test is from the OpenAQ doc
def testOpenAQ():

  url = "https://api.openaq.org/v2/measurements?date_to=2023-10-03T18%3A14%3A00Z&limit=100&page=1&offset=0&sort=desc&radius=1000&order_by=datetime"

  headers = {"accept": "application/json"}

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    # Convert the response to JSON format
    print("Success!")
  else:
    print(f"Error: Failed to fetch data from the API. Status code: {response.status_code}")


def fetchOneMonth(data, params):
    api_key = "9203abc1267cb56ec6c9f843271ceef8ce4d3c445923782a5b491296a6f07386"

    # Define the API URL and Header
    api_url = "https://api.openaq.org/v2/measurements"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Define the date range until now
    end_date = datetime.now()

    # Initialize an empty list to store data
    data_list = []

    # Iterate through the data dictionary
    for city, location_id, start_date in zip(data["nearest_city"], data["Location ID"], data["Start Date"]):
        params["location_id"] = location_id

        # Create a new dictionary to store location name, ID, and data
        location_data = {
            "Location": city,
            "Location_ID": location_id,
            "Data": []  # To store measurement data for this location
        }


        while start_date < end_date:
          params["date_from"] = start_date.isoformat() + "Z"

          # Increment the date by three months for the next request
          start_date += timedelta(days=60)  # Interval set to 1 month

          # Set the end_date for each request as the minimum of the next 1 months or the current end_date
          params["date_to"] = min((start_date, end_date)).isoformat() + "Z"
          print(params)
          break

          # Send the API request
          response = requests.get(api_url, params=params, headers=headers)

          # Check if the request was successful (status code 200)
          if response.status_code == 200:
              # Convert the response to JSON format
              data = response.json()
              measurements = data.get("results", [])
              location_data["Data"].extend(measurements)
          else:
              print(f"Error: Failed to fetch data from the API. Status code: {response.status_code}")
              break
          # print(location_data)

          # Introduce a delay of 5 seconds before the next request
          time.sleep(5)
        break
        # Add the location's data dictionary to the main data list
        data_list.append(location_data)

    return data_list

def load_sensor_data():
  # fetch sensors.csv from s3
  # drive.mount('/content/gdrive')
  df=pd.read_csv('sensors_complete.csv')

  return df

def lambda_handler(event, context):
    df = load_sensor_data()
    # Define the parameters for the API request
    params = {
        "parameter": ["pm10", "um003", "humidity", "pm1", "um025", "pm25", "um010", "um050", "um100", "temperature", "pressure", "um005"],
        "limit": 10000  # Increase the limit to get more data per request
    }
    # data_list = fetchData(cities, params)
    data_list = fetchOneMonth(df, params)
    file_name = 'sensor_data_month.json'
    bucket_name = 'openaq-demo'

    return {
        'statusCode': 200,
        'body': "Payload written to s3"
    }

df = load_sensor_data()
#df['Start Date'] = pd.to_datetime(df['Start Date']).dt.tz_localize('UTC')
df['Start Date'] = pd.to_datetime(df['Start Date']).dt.tz_localize(None)

# Define the parameters for the API request
params = {
    "parameter": ["pm25"],
    "limit": 10000  # Increase the limit to get more data per request
}
# data_list = fetchData(cities, params)
# data_list = fetchOneMonth(df, params)

# testOpenAQ()

testAPI()

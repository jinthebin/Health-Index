
import requests
import pandas as pd
# define function to make API call:
def fetch_json_from_api(url):
    try:
        # Send a GET request to the API endpoint
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()
            return json_data
        else:
            print(f"Error: Unable to fetch data, Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Exception occurred: {e}")
        return None

api_url = "https://fingertips.phe.org.uk/api/all_data/csv/for_one_indicator?indicator_id=%7B%7D" 
ph_england = fetch_json_from_api(api_url)
nihr_data = pd.json_normalize(ph_england)
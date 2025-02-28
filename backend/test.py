import requests
import json
from serpapi import GoogleSearch
def test1():
    url = "https://api.makcorps.com/mapping"
    params = {
        'api_key': '67b709fed6364c5254375d8a',
        'name': 'istanbul'
    }

    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        json_data = response.json()
        with open ('data.json', 'w') as f:
            json.dump(json_data, f)
        
        # Print or use the parsed JSON data
        print(json_data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
def test2():

    url = "https://api.makcorps.com/city"
    params = {
        'cityid': '293974',
        'pagination': '0',
        'cur': 'TRY',
        'rooms': '1',
        'adults': '2',
        'checkin': '2025-02-26',
        'checkout': '2025-03-01',
        'api_key': '67b709fed6364c5254375d8a'
    }

    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        json_data = response.json()
        with open ('data.json', 'w') as f:
            json.dump(json_data, f)
        
        # Print or use the parsed JSON data
        print(json_data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
# test2()
def test3():
    

    params = {
    "engine": "google_hotels",
    "q": "Ankara",
    "check_in_date": "2025-02-26",
    "check_out_date": "2025-02-27",
    "adults": "2",
    "currency": "TRY",
    "gl": "us",
    "hl": "en",
    "api_key": "78060ba18068658676f6fb5b9aa2e0c0753ca067bb8aae6bd3950659fd466b50"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    
    with open ('data.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
def test4():
    # from serpapi import GoogleSearch

    params = {
    "engine": "google_hotels",
    "q": "The Green Park Hotel Ankara",
    "check_in_date": "2025-02-27",
    "check_out_date": "2025-02-28",
    "adults": "2",
    "currency": "USD",
    "gl": "us",
    "hl": "en",
    "api_key": "78060ba18068658676f6fb5b9aa2e0c0753ca067bb8aae6bd3950659fd466b50"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    with open ('data.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
test4()
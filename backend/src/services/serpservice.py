import json
from serpapi import GoogleSearch
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed
from datetime import datetime
class SerpService():
    def __init__(self, api_key):
        self.api_key = api_key
        
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def search_city(self,location:str,check_in:str,check_out:str):
        try:
            # print(check_in)
            check_in =  datetime.now().strftime("%Y") + "-" + check_in
            check_out =  datetime.now().strftime("%Y") + "-" + check_out
            # check_out = check_out + "-" + datetime.now().strftime("%Y")
            # print(check_in)
            # print(check_out)
            params = {
                "engine": "google_hotels",
                "q": location,
                "check_in_date": f"{check_in}",
                "check_out_date": f"{check_out}",
                # "adults": adults,
                "currency": "TRY",
                "gl": "tr",
                "hl": "tr",
                "api_key": self.api_key
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            with open ('data2.json', 'w') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            # print(results)
            return results
        except Exception as e:
            print(e)
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def hotel_prices_details(self,hotel_name:str,check_in:str,check_out:str):
        params = {
            "engine": "google_hotels",
            "q": hotel_name,
            "check_in_date": check_in,
            "check_out_date": check_out,
            # "adults": adults,
            "currency": "TRY",
            "gl": "tr",
            "hl": "tr",
            "api_key": self.api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def very_details(self,property_key:str,city_name:str,check_in:str,check_out:str):
        check_in =  datetime.now().strftime("%Y") + "-" + check_in
        check_out =  datetime.now().strftime("%Y") + "-" + check_out
        params = {
            "engine": "google_hotels",
            "q": city_name,
            "check_in_date": check_in,
            "check_out_date": check_out,
            # "adults": adults,
            "currency": "TRY",
            "gl": "tr",
            "hl": "tr",
            "property_token": property_key,
            "api_key": self.api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        with open ('data3.json', 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        return results
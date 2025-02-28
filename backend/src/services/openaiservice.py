from openai import AzureOpenAI
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed
from src.core.config import settings
import json
from src.database.schemas import HotelResponseList
class OpenAIService():
    def __init__(self,endpoint:str,key:str,model:str,version:str):
        self.endpoint = endpoint
        self.key = key
        self.model = model
        self.version = version
        
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def find_hotels(self,question:str):
        from src.services.serpservice import SerpService
        serp = SerpService(api_key=settings.hotels_apikey)
        
        conversation = [
                {
                "role": "system",
                "content": f"""
                You are an AI assistant that helps me find hotels in a given location and for specified dates.  
                I will provide you with the check-in and check-out dates along with the location,  
                and you will use a tool call to retrieve and list the available hotel prices for me.
                
                Write all hotels from returned tool.
                """
                },
                {
                    "role": "user",
                    "content": f"{question}"
                }
            ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "hotel_search",
                    "description": "Search for hotels in a given location and for specified dates.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location where you want to find hotels."
                            },
                            "check_in": {
                                "type": "string",
                                "description": "The check-in date for the hotel stay. Format: -DD (e.g., 02-28 for February 28)."
                            },
                            "check_out": {
                                "type": "string",
                                "description": "The check-out date for the hotel stay. Format: MM-DD (e.g., 03-02 for March 2)."
                            }
                        },
                        "required": ["location", "check_in", "check_out"],
                        "additionalProperties": False  # Bu satır eklendi
                    },
                    "strict": True  # Bunu koruyoruz
                }
            }
        ]
        available_functions = {
            "hotel_search": serp.search_city
        }
        client = AzureOpenAI(azure_endpoint=self.endpoint,api_key=self.key,api_version=self.version)
        try:
            response = client.beta.chat.completions.parse(
                model=self.model,
                messages=conversation,
                tools=tools,
                tool_choice="auto",
                temperature=0.2
            )
            
            tool_call = response.choices[0].message.tool_calls
            if tool_call:
                tool_call = tool_call[0]
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print(function_args)
                city = function_args["location"]
                check_in = function_args["check_in"]
                check_out = function_args["check_out"]
                arguments = {
                    "city": city,
                    "check_in": check_in,
                    "check_out": check_out
                }

                function_response = function_to_call(**function_args)
                conversation.append({
                    "tool_call_id": tool_call.id,
                    "role": "function",
                    "name": tool_call.function.name,
                    "content": json.dumps(function_response,ensure_ascii=False)
                })
                
            second_response = client.beta.chat.completions.parse(
                model=self.model,
                messages=conversation,
                tools=tools,
                tool_choice="auto",
                temperature=0.2,
                response_format=HotelResponseList
            )
            return {
                "response": second_response.choices[0].message.parsed,
                "arguments": arguments
            }
            # endpointleri yazmadan devam edeceksin.
            
            # buradan devam edilecek.
        except Exception as e:
            return {"error": str(e)}
        
        # schemas'da structured outputu ayarla. liste şeklinde.
    # burada yapılacak olan şey iki tane tool_call olacak.
    # otel veya şehir adına göre arama yapılacak iki tool_call olma sebebi bu
    # ardından structured output olarak çıktı vereceksin ve bu çıktıyı döndüreceksin.
    # detay linki olacak orada direkt property token'ı alıp yeni arama yapıp detay döndüreceksin
    # detayda fiyatlar linkler gibi bilgiler yer alacak.
        
        
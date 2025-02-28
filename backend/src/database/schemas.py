from pydantic import BaseModel,Field
from typing import List,Dict
class HotelResponse(BaseModel):
    hotel_name : str = Field(...,title="Hotel name e.g. Hilton")
    total_price_without_tax : str = Field(...,title="Total hotel price without tax. Firstly, You see total_rate after extracted_before_taxes_fees.")
    total_price_with_tax : str = Field(...,title="Total hotel price after taxes fees. You see total_rate after you see lowest. It is the total price of the hotel with tax.")
    rating : str = Field(...,title="Hotel rating")
    hotel_class : str = Field(...,title="Hotel class e.g. X-star")
    property_token : str = Field(...,title="API hotel property token")
    # city: str = Field(...,title="City name")
    # check_in: str = Field(...,title="Check in date")
    # check_out: str = Field(...,title="Check out date")
    
class HotelResponseList(BaseModel):
    response : List[HotelResponse] = Field(...,title="List of hotel responses")
# hotelresponse'u oluştur. structured outputumuz o olacak.
from pydantic import BaseModel

class MotivationResponse(BaseModel):
    motivation: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "motivation": "Wellness begins with simple actions. Start today and change your tomorrow."
            }
        }
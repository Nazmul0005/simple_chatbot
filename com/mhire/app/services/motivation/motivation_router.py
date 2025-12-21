from fastapi import APIRouter, HTTPException
from com.mhire.app.services.motivation.motivation import motivation_service
from com.mhire.app.services.motivation.motivation_schema import MotivationResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["Motivation"]
)

@router.get("/motivation", response_model=MotivationResponse)
async def get_motivation():
    """
    Generate a daily motivational quote for habit tracking
    
    Returns a short 1-2 sentence motivational message to inspire users
    in their habit-building journey.
    """
    try:
        motivation_text = await motivation_service.generate_motivation()
        return MotivationResponse(motivation=motivation_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate motivation: {str(e)}"
        )
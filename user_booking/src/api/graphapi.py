from fastapi.requests import Request
from fastapi import HTTPException
from fastapi.routing import APIRouter
from src.models.agentsModels import userQuery
from src.pipeline.bookingsystem import  Bookingsystempipeline
booking_api_router = APIRouter(tags=["Bookingsystem"])
booking_pipeline=Bookingsystempipeline()

@booking_api_router.post("/get_response" )
def get_response(request: userQuery):
    try:
        response=booking_pipeline.get_response(user_query=request.user_query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
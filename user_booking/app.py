from fastapi import FastAPI
from src.api.graphapi import booking_api_router 
import uvicorn
app=FastAPI()


app.include_router(booking_api_router, prefix="/getresponse")

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0", timeout_keep_alive=300, timeout_graceful_shutdown=600)

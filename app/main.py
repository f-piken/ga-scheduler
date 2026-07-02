from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GenerateScheduleRequest(BaseModel):
    jamaahs: list
    team_leaders: list
    muthowifs: list
    departures: list

@app.post("/generate-schedule")
def generate_schedule(request: GenerateScheduleRequest):

    return {
        "status": "success",
        "received_data": {
            "jamaahs": request.jamaahs,
            "team_leaders": request.team_leaders,
            "muthowifs": request.muthowifs,
            "departures": request.departures
        }
    }
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GenerateScheduleRequest(BaseModel):
    jamaahs: list
    team_leaders: list
    muthowifs: list
    departures: list

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/generate-schedule")
def generate_schedule(request: GenerateScheduleRequest):

    from app.services.scheduler import SchedulerService

    result = SchedulerService.generate(
        jamaahs=request.jamaahs,
        team_leaders=request.team_leaders,
        muthowifs=request.muthowifs,
        departures=request.departures
    )

    return result
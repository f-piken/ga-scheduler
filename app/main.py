from fastapi import FastAPI
from pydantic import BaseModel

from app.services.scheduler import SchedulerService

app = FastAPI()


class GenerateScheduleRequest(BaseModel):

    jamaahs: list

    team_leaders: list

    muthowifs: list

    departures: list


@app.get("/generate-schedule")
def generate_schedule(
    request: GenerateScheduleRequest
):

    result = SchedulerService.generate(

        jamaahs=request.jamaahs,

        team_leaders=request.team_leaders,

        muthowifs=request.muthowifs,

        departures=request.departures

    )

    return result
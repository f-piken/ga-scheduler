# main.py

from app.services.scheduler import SchedulerService

def generate(data):

    return SchedulerService.generate(
        jamaahs=data["jamaahs"],
        team_leaders=data["team_leaders"],
        muthowifs=data["muthowifs"],
        departures=data["departures"]
    )
from pydantic import BaseModel
from typing import List, Dict


class ScheduleRequest(BaseModel):

    jamaahs: List[Dict]

    team_leaders: List[Dict]

    muthowifs: List[Dict]

    departures: List[Dict]
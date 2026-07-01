# app/services/scheduler.py

from app.core.ga import GeneticAlgorithm


class SchedulerService:

    @staticmethod
    def generate(
        jamaahs,
        team_leaders,
        muthowifs,
        departures
    ):

        ga = GeneticAlgorithm(

            jamaahs=jamaahs,

            team_leaders=team_leaders,

            muthowifs=muthowifs,

            departures=departures,
        )

        return ga.run()
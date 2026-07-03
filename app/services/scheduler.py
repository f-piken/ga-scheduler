from app.core.ga import GeneticAlgorithm


class SchedulerService:

    @staticmethod
    def generate(
        jamaahs,
        team_leaders,
        muthowifs,
        departures
    ):
        
        for d in departures:
            d["quota"] = int(d["quota"])
            d["remaining_quota"] = int(d["remaining_quota"])
            
        ga = GeneticAlgorithm(
            jamaahs=jamaahs,
            team_leaders=team_leaders,
            muthowifs=muthowifs,
            departures=departures,
        )

        return ga.run()
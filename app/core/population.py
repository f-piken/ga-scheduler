import random


class PopulationGenerator:

    @staticmethod
    def create_gene(
        jamaah,
        team_leaders,
        muthowifs,
        departures,
        departure_team_leader_map,
        departure_muthowif_map
    ):

        # =====================================
        # FILTER PAKET SESUAI JAMAAH
        # =====================================

        matching_departures = [

            departure

            for departure in departures

            if (

                departure["paket_id"]
                ==
                jamaah["paket_id"]

                and

                departure["remaining_quota"] > 0

            )

        ]

        if matching_departures:

            departure = random.choice(
                matching_departures
            )

        else:

            departure = random.choice(
                departures
            )

        departure_id = departure["id"]

        # =====================================
        # 1 KEBERANGKATAN = 1 TEAM LEADER
        # =====================================

        if departure_id not in departure_team_leader_map:

            active_team_leaders = [

                tl

                for tl in team_leaders

                if tl["status"] == "available"

            ]

            if active_team_leaders:

                departure_team_leader_map[
                    departure_id
                ] = random.choice(
                    active_team_leaders
                )

            else:

                departure_team_leader_map[
                    departure_id
                ] = random.choice(
                    team_leaders
                )

        team_leader = departure_team_leader_map[
            departure_id
        ]

        # =====================================
        # 1 KEBERANGKATAN = 1 MUTHOWIF
        # =====================================

        if departure_id not in departure_muthowif_map:

            active_muthowifs = [

                m

                for m in muthowifs

                if m["status"] == "Aktif"

            ]

            if active_muthowifs:

                departure_muthowif_map[
                    departure_id
                ] = random.choice(
                    active_muthowifs
                )

            else:

                departure_muthowif_map[
                    departure_id
                ] = random.choice(
                    muthowifs
                )

        muthowif = departure_muthowif_map[
            departure_id
        ]

        # =====================================
        # CREATE GENE
        # =====================================

        return {

            # JAMAAH

            "jamaah_id":
                jamaah["id"],

            "jamaah_name":
                jamaah["name"],

            "jamaah_paket_id":
                jamaah["paket_id"],

            # TEAM LEADER

            "team_leader_id":
                team_leader["id"],

            "team_leader_name":
                team_leader["name"],

            "team_leader_status":
                team_leader["status"],

            # MUTHOWIF

            "muthowif_id":
                muthowif["id"],

            "muthowif_name":
                muthowif["name"],

            "muthowif_status":
                muthowif["status"],

            # KEBERANGKATAN

            "departure_id":
                departure["id"],

            "departure_paket_id":
                departure["paket_id"],

            "departure_date":
                departure["departure_date"],

            "quota":
                departure["quota"],

            "remaining_quota":
                departure["remaining_quota"],

            "departure_status":
                departure["status"]
        }

    @staticmethod
    def create_chromosome(
        jamaahs,
        team_leaders,
        muthowifs,
        departures
    ):

        chromosome = []

        departure_team_leader_map = {}

        departure_muthowif_map = {}

        for jamaah in jamaahs:

            gene = PopulationGenerator.create_gene(

                jamaah,

                team_leaders,

                muthowifs,

                departures,

                departure_team_leader_map,

                departure_muthowif_map

            )

            chromosome.append(
                gene
            )

        return chromosome

    @staticmethod
    def generate_population(
        population_size,
        jamaahs,
        team_leaders,
        muthowifs,
        departures
    ):

        population = []

        logs = []

        for i in range(population_size):

            chromosome = (
                PopulationGenerator.create_chromosome(

                    jamaahs,

                    team_leaders,

                    muthowifs,

                    departures

                )
            )

            population.append(
                chromosome
            )

            logs.append({

                "population_index":
                    i + 1,

                "chromosome":
                    chromosome

            })

        return population, logs
import random


class Mutation:

    @staticmethod
    def random_gene_mutation(
        chromosome,
        team_leaders,
        muthowifs,
        departures
    ):

        # =====================================
        # RANDOM GENE
        # =====================================

        mutation_index = random.randint(
            0,
            len(chromosome) - 1
        )

        old_gene = chromosome[
            mutation_index
        ].copy()

        gene = chromosome[
            mutation_index
        ]

        # =====================================
        # TEAM LEADER AKTIF
        # =====================================

        active_team_leaders = [

            tl

            for tl in team_leaders

            if tl["status"] == "available"

        ]

        if active_team_leaders:

            team_leader = random.choice(
                active_team_leaders
            )

        else:

            team_leader = random.choice(
                team_leaders
            )

        # =====================================
        # MUTHOWIF AKTIF
        # =====================================

        active_muthowifs = [

            m

            for m in muthowifs

            if m["status"] == "available"

        ]

        if active_muthowifs:

            muthowif = random.choice(
                active_muthowifs
            )

        else:

            muthowif = random.choice(
                muthowifs
            )

        # =====================================
        # DEPARTURE SESUAI PAKET
        # =====================================

        matching_departures = [

            departure

            for departure in departures

            if (

                departure["paket_id"]

                ==

                gene.get(
                    "jamaah_paket_id"
                )

                and

                departure[
                    "remaining_quota"
                ] > 0

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

        # =====================================
        # UPDATE TEAM LEADER
        # =====================================

        gene["team_leader_id"] = \
            team_leader["id"]

        gene["team_leader_name"] = \
            team_leader["name"]

        gene["team_leader_status"] = \
            team_leader["status"]

        # =====================================
        # UPDATE MUTHOWIF
        # =====================================

        gene["muthowif_id"] = \
            muthowif["id"]

        gene["muthowif_name"] = \
            muthowif["name"]

        gene["muthowif_status"] = \
            muthowif["status"]

        # =====================================
        # UPDATE DEPARTURE
        # =====================================

        gene["departure_id"] = \
            departure["id"]

        gene["departure_paket_id"] = \
            departure["paket_id"]

        gene["departure_date"] = \
            departure["departure_date"]

        gene["quota"] = \
            departure["quota"]

        gene["remaining_quota"] = \
            departure["remaining_quota"]

        gene["departure_status"] = \
            departure["status"]

        # =====================================
        # NEW GENE
        # =====================================

        new_gene = gene.copy()

        logs = {

            "mutation_index":
                mutation_index,

            "before":
                old_gene,

            "after":
                new_gene

        }

        return chromosome, logs
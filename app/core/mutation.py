from collections import defaultdict
import random

class Mutation:

    @staticmethod
    def random_gene_mutation(
        chromosome,
        team_leaders,
        muthowifs,
        departures
    ):

        if len(chromosome) == 0:

            return chromosome, {}

        tl_usage = defaultdict(int)
        muthowif_usage = defaultdict(int)
        departure_usage = defaultdict(int)

        for gene in chromosome:

            tl_usage[
                gene["team_leader_id"]
            ] += 1

            muthowif_usage[
                gene["muthowif_id"]
            ] += 1

            departure_usage[
                gene["departure_id"]
            ] += 1

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

        paket_id = gene[
            "jamaah_paket_id"
        ]

        valid_departures = []

        for departure in departures:

            if (

                departure["paket_id"]
                ==
                paket_id

                and

                str(
                    departure["status"]
                ).lower()
                ==
                "open"

            ):

                current = departure_usage[
                    departure["id"]
                ]

                quota = departure[
                    "quota"
                ]

                if current < quota:

                    valid_departures.append(
                        departure
                    )

        if valid_departures:

            departure = min(

                valid_departures,

                key=lambda d:
                departure_usage[
                    d["id"]
                ]

            )

        else:

            departure = random.choice(
                departures
            )

        available_tls = [

            tl

            for tl in team_leaders

            if str(
                tl["status"]
            ).lower()
            ==
            "available"

        ]

        if not available_tls:

            available_tls = (
                team_leaders
            )

        team_leader = min(

            available_tls,

            key=lambda tl:
            tl_usage[
                tl["id"]
            ]

        )

        available_muthowifs = [

            m

            for m in muthowifs

            if str(
                m["status"]
            ).lower()
            in [
                "aktif",
                "available"
            ]

        ]

        if not available_muthowifs:

            available_muthowifs = (
                muthowifs
            )

        muthowif = min(

            available_muthowifs,

            key=lambda m:
            muthowif_usage[
                m["id"]
            ]

        )

        gene["team_leader_id"] = \
            team_leader["id"]

        gene["team_leader_name"] = \
            team_leader["name"]

        gene["team_leader_status"] = \
            team_leader["status"]

        gene["muthowif_id"] = \
            muthowif["id"]

        gene["muthowif_name"] = \
            muthowif["name"]

        gene["muthowif_status"] = \
            muthowif["status"]

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

        logs = {

            "mutation_index":
                mutation_index,

            "before":
                old_gene,

            "after":
                gene.copy()

        }

        return chromosome, logs
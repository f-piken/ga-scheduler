import random


class Repair:

    @staticmethod
    def repair_schedule(
        chromosome,
        departures
    ):

        repaired_chromosome = []

        # =====================================
        # REPAIR PAKET & DEPARTURE
        # =====================================

        for gene in chromosome:

            jamaah_paket_id = gene.get(
                "jamaah_paket_id"
            )

            departure_paket_id = gene.get(
                "departure_paket_id"
            )

            departure_status = gene.get(
                "departure_status"
            )

            remaining_quota = gene.get(
                "remaining_quota",
                0
            )

            invalid = (

                jamaah_paket_id
                !=
                departure_paket_id

                or

                departure_status != "open"

                or

                remaining_quota <= 0

            )

            if invalid:

                valid_departures = [

                    departure

                    for departure in departures

                    if (

                        departure["paket_id"]
                        ==
                        jamaah_paket_id

                        and

                        departure["status"]
                        ==
                        "open"

                        and

                        departure[
                            "remaining_quota"
                        ] > 0

                    )

                ]

                if valid_departures:

                    departure = random.choice(
                        valid_departures
                    )

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

            repaired_chromosome.append(
                gene
            )

        # =====================================
        # 1 DEPARTURE = 1 TEAM LEADER
        # =====================================

        departure_team_leader_map = {}

        # =====================================
        # 1 DEPARTURE = 1 MUTHOWIF
        # =====================================

        departure_muthowif_map = {}

        for gene in repaired_chromosome:

            departure_id = gene.get(
                "departure_id"
            )

            # =================================
            # TEAM LEADER
            # =================================

            if departure_id not in \
                departure_team_leader_map:

                departure_team_leader_map[
                    departure_id
                ] = {

                    "team_leader_id":
                    gene.get(
                        "team_leader_id"
                    ),

                    "team_leader_name":
                    gene.get(
                        "team_leader_name"
                    ),

                    "team_leader_status":
                    gene.get(
                        "team_leader_status"
                    )

                }

            else:

                gene["team_leader_id"] = \
                    departure_team_leader_map[
                        departure_id
                    ]["team_leader_id"]

                gene["team_leader_name"] = \
                    departure_team_leader_map[
                        departure_id
                    ]["team_leader_name"]

                gene["team_leader_status"] = \
                    departure_team_leader_map[
                        departure_id
                    ]["team_leader_status"]

            # =================================
            # MUTHOWIF
            # =================================

            if departure_id not in \
                departure_muthowif_map:

                departure_muthowif_map[
                    departure_id
                ] = {

                    "muthowif_id":
                    gene.get(
                        "muthowif_id"
                    ),

                    "muthowif_name":
                    gene.get(
                        "muthowif_name"
                    ),

                    "muthowif_status":
                    gene.get(
                        "muthowif_status"
                    )

                }

            else:

                gene["muthowif_id"] = \
                    departure_muthowif_map[
                        departure_id
                    ]["muthowif_id"]

                gene["muthowif_name"] = \
                    departure_muthowif_map[
                        departure_id
                    ]["muthowif_name"]

                gene["muthowif_status"] = \
                    departure_muthowif_map[
                        departure_id
                    ]["muthowif_status"]

        return repaired_chromosome
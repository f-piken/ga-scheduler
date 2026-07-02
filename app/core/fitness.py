from collections import Counter


class FitnessCalculator:

    @staticmethod
    def calculate(chromosome):

        total_penalty = 0

        team_leader_usage = []
        muthowif_usage = []

        departure_usage = {}

        # =====================================
        # LOOP GENE
        # =====================================

        for gene in chromosome:

            team_leader_id = gene.get(
                "team_leader_id"
            )

            muthowif_id = gene.get(
                "muthowif_id"
            )

            departure_id = gene.get(
                "departure_id"
            )

            team_leader_usage.append(
                team_leader_id
            )

            muthowif_usage.append(
                muthowif_id
            )

            departure_usage[
                departure_id
            ] = departure_usage.get(
                departure_id,
                0
            ) + 1

            # =================================
            # PAKET SESUAI
            # =================================

            if (
                gene.get("jamaah_paket_id")
                !=
                gene.get("departure_paket_id")
            ):

                total_penalty += 1

            # =================================
            # STATUS KEBERANGKATAN
            # =================================

            departure_status = gene.get(
                "departure_status",
                "open"
            )

            if departure_status == "closed":

                total_penalty += 0.6

            elif departure_status == "full":

                total_penalty += 0.6

            # =================================
            # SISA KUOTA
            # =================================

            remaining_quota = gene.get(
                "remaining_quota",
                0
            )

            if remaining_quota <= 0:

                total_penalty += 0.4

            elif remaining_quota <= 5:

                total_penalty += 0.05

            # =================================
            # TEAM LEADER STATUS
            # =================================

            tl_status = gene.get(
                "team_leader_status",
                "available"
            )

            if tl_status == "busy":

                total_penalty += 0.3

            elif tl_status == "inactive":

                total_penalty += 0.6

            # =================================
            # MUTHOWIF STATUS
            # =================================

            muthowif_status = gene.get(
                "muthowif_status",
                "available"
            )

            if muthowif_status == "busy":

                total_penalty += 0.3

            elif muthowif_status == "inactive":

                total_penalty += 0.6

        # =====================================
        # KONFLIK TEAM LEADER
        # =====================================

        tl_counter = Counter(
            team_leader_usage
        )

        for _, total in tl_counter.items():

            if total > 1:

                total_penalty += (
                    (total - 1) * 0.05
                )

        # =====================================
        # KONFLIK MUTHOWIF
        # =====================================

        muthowif_counter = Counter(
            muthowif_usage
        )

        for _, total in muthowif_counter.items():

            if total > 1:

                total_penalty += (
                    (total - 1) * 0.05
                )

        # =====================================
        # OVERLOAD KUOTA
        # =====================================

        for gene in chromosome:

            departure_id = gene.get(
                "departure_id"
            )

            quota = gene.get(
                "quota",
                0
            )

            total_jamaah = departure_usage.get(
                departure_id,
                0
            )

            if total_jamaah > quota:

                overload = (
                    total_jamaah - quota
                )

                total_penalty += (
                    overload * 0.8
                )

        # =====================================
        # FITNESS
        # =====================================

        fitness = 1 / (
            1 + total_penalty
        )

        return round(
            fitness,
            5
        )
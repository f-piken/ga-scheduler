from collections import defaultdict
from datetime import datetime
import statistics


class FitnessCalculator:

    MAX_JAMAAH_PER_TL = 40
    MAX_JAMAAH_PER_MUTHOWIF = 40

    @staticmethod
    def calculate(chromosome):

        total_penalty = 0

        departure_usage = defaultdict(int)
        tl_usage = defaultdict(int)
        muthowif_usage = defaultdict(int)

        departure_data = {}

        for gene in chromosome:

            departure_id = gene.get("departure_id")
            tl_id = gene.get("team_leader_id")
            muthowif_id = gene.get("muthowif_id")

            departure_usage[departure_id] += 1
            tl_usage[tl_id] += 1
            muthowif_usage[muthowif_id] += 1

            if departure_id not in departure_data:

                departure_data[departure_id] = {

                    "date":
                        gene.get("departure_date"),

                    "team_leader_id":
                        tl_id,

                    "muthowif_id":
                        muthowif_id,

                    "quota":
                        gene.get("quota", 0)

                }

            # Paket harus sesuai

            if (
                gene.get("jamaah_paket_id")
                !=
                gene.get("departure_paket_id")
            ):

                total_penalty += 1

            # Departure harus open

            if (
                str(
                    gene.get(
                        "departure_status",
                        ""
                    )
                ).lower()
                !=
                "open"
            ):

                total_penalty += 1

            # TL harus available

            if (
                str(
                    gene.get(
                        "team_leader_status",
                        ""
                    )
                ).lower()
                !=
                "available"
            ):

                total_penalty += 1

            # Muthowif harus available

            if (
                str(
                    gene.get(
                        "muthowif_status",
                        ""
                    )
                ).lower()
                !=
                "available"
            ):

                total_penalty += 1

        for tl_id, total in tl_usage.items():

            if total > FitnessCalculator.MAX_JAMAAH_PER_TL:

                overload = (
                    total
                    -
                    FitnessCalculator.MAX_JAMAAH_PER_TL
                )

                total_penalty += (
                    overload * 0.2
                )

            else:

                unused = (
                    FitnessCalculator.MAX_JAMAAH_PER_TL
                    -
                    total
                )

                total_penalty += (
                    unused * 0.003
                )

        for muthowif_id, total in (
            muthowif_usage.items()
        ):

            if total > FitnessCalculator.MAX_JAMAAH_PER_MUTHOWIF:

                overload = (
                    total
                    -
                    FitnessCalculator.MAX_JAMAAH_PER_MUTHOWIF
                )

                total_penalty += (
                    overload * 0.2
                )

            else:

                unused = (
                    FitnessCalculator.MAX_JAMAAH_PER_MUTHOWIF
                    -
                    total
                )

                total_penalty += (
                    unused * 0.003
                )

        for departure_id, total in (
            departure_usage.items()
        ):

            quota = departure_data[
                departure_id
            ]["quota"]

            if total > quota:

                overload = total - quota

                total_penalty += (
                    overload * 0.5
                )

        departure_totals = list(
            departure_usage.values()
        )

        if len(departure_totals) > 1:

            std_dev = statistics.pstdev(
                departure_totals
            )

            total_penalty += (
                std_dev * 0.05
            )

        departures = list(
            departure_data.values()
        )

        for i in range(
            len(departures)
        ):

            for j in range(
                i + 1,
                len(departures)
            ):

                dep1 = departures[i]
                dep2 = departures[j]

                try:

                    date1 = datetime.strptime(
                        dep1["date"],
                        "%Y-%m-%d"
                    )

                    date2 = datetime.strptime(
                        dep2["date"],
                        "%Y-%m-%d"
                    )

                except Exception:

                    continue

                diff_days = abs(
                    (
                        date1 - date2
                    ).days
                )

                # Team Leader bentrok

                if (

                    dep1["team_leader_id"]
                    ==
                    dep2["team_leader_id"]

                    and

                    diff_days <= 21

                ):

                    total_penalty += 0.5

                # Muthowif bentrok

                if (

                    dep1["muthowif_id"]
                    ==
                    dep2["muthowif_id"]

                    and

                    diff_days <= 21

                ):

                    total_penalty += 0.5

        fitness = 1 / (
            1 + total_penalty
        )

        return round(
            fitness,
            8
        )
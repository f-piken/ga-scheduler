from collections import defaultdict
from datetime import datetime
import math

class Repair:

    MAX_JAMAAH_PER_TL = 40
    MAX_JAMAAH_PER_MUTHOWIF = 40

    @staticmethod
    def repair_schedule(
        chromosome,
        departures,
        team_leaders,
        muthowifs
    ):

        if not chromosome:
            return chromosome

        departure_usage = defaultdict(int)

        for gene in chromosome:

            departure_usage[
                gene["departure_id"]
            ] += 1

        # =====================================
        # PERBAIKI DEPARTURE INVALID
        # =====================================

        for gene in chromosome:

            paket_id = gene[
                "jamaah_paket_id"
            ]

            current_departure = gene[
                "departure_id"
            ]

            departure_status = str(
                gene.get(
                    "departure_status",
                    ""
                )
            ).lower()

            valid_departures = []

            for departure in departures:

                if (

                    departure["paket_id"]
                    == paket_id

                    and

                    str(
                        departure["status"]
                    ).lower()
                    == "open"

                ):

                    current_count = (
                        departure_usage[
                            departure["id"]
                        ]
                    )

                    if (
                        current_count
                        <
                        departure["quota"]
                    ):

                        valid_departures.append(
                            departure
                        )

            invalid = (

                gene[
                    "jamaah_paket_id"
                ]

                !=

                gene[
                    "departure_paket_id"
                ]

                or

                departure_status
                !=
                "open"

            )

            if invalid and valid_departures:

                best_departure = min(

                    valid_departures,

                    key=lambda d:
                    departure_usage[
                        d["id"]
                    ]

                )

                departure_usage[
                    current_departure
                ] -= 1

                departure_usage[
                    best_departure["id"]
                ] += 1

                gene["departure_id"] = (
                    best_departure["id"]
                )

                gene["departure_paket_id"] = (
                    best_departure["paket_id"]
                )

                gene["departure_date"] = (
                    best_departure[
                        "departure_date"
                    ]
                )

                gene["quota"] = (
                    best_departure["quota"]
                )

                gene["remaining_quota"] = (
                    best_departure[
                        "remaining_quota"
                    ]
                )

                gene["departure_status"] = (
                    best_departure["status"]
                )

        # =====================================
        # PERBAIKI OVERLOAD QUOTA
        # =====================================

        changed = True

        while changed:

            changed = False

            for departure in departures:

                dep_id = departure["id"]

                quota = departure[
                    "quota"
                ]

                total = departure_usage[
                    dep_id
                ]

                if total <= quota:
                    continue

                overload = total - quota

                moved = 0

                for gene in chromosome:

                    if moved >= overload:
                        break

                    if (
                        gene["departure_id"]
                        != dep_id
                    ):
                        continue

                    paket_id = gene[
                        "jamaah_paket_id"
                    ]

                    candidates = [

                        d

                        for d in departures

                        if (

                            d["paket_id"]
                            == paket_id

                            and

                            str(
                                d["status"]
                            ).lower()
                            == "open"

                            and

                            departure_usage[
                                d["id"]
                            ]
                            <
                            d["quota"]

                        )

                    ]

                    if not candidates:
                        continue

                    target = min(

                        candidates,

                        key=lambda d:
                        departure_usage[
                            d["id"]
                        ]

                    )

                    departure_usage[
                        dep_id
                    ] -= 1

                    departure_usage[
                        target["id"]
                    ] += 1

                    gene["departure_id"] = (
                        target["id"]
                    )

                    gene["departure_paket_id"] = (
                        target["paket_id"]
                    )

                    gene["departure_date"] = (
                        target[
                            "departure_date"
                        ]
                    )

                    gene["quota"] = (
                        target["quota"]
                    )

                    gene["remaining_quota"] = (
                        target[
                            "remaining_quota"
                        ]
                    )

                    gene["departure_status"] = (
                        target["status"]
                    )

                    moved += 1
                    changed = True

        # =====================================
        # GROUP PER DEPARTURE
        # =====================================

        departure_groups = defaultdict(list)

        for gene in chromosome:

            departure_groups[
                gene["departure_id"]
            ].append(gene)

        # =====================================
        # TL AVAILABLE
        # =====================================

        available_tls = [

            tl

            for tl in team_leaders

            if str(
                tl["status"]
            ).lower()
            == "available"

        ]

        if not available_tls:

            available_tls = (
                team_leaders
            )

        # =====================================
        # MUTHOWIF AVAILABLE
        # =====================================

        available_muthowifs = [

            m

            for m in muthowifs

            if str(
                m["status"]
            ).lower()
            in [
                "available",
                "aktif"
            ]

        ]

        if not available_muthowifs:

            available_muthowifs = (
                muthowifs
            )

                # =====================================
        # TRACKING JADWAL TL & MUTHOWIF
        # =====================================

        tl_schedule = defaultdict(list)
        muthowif_schedule = defaultdict(list)

        # =====================================
        # REBALANCE TL
        # =====================================

        for departure_id, jamaahs in departure_groups.items():

            departure_date = jamaahs[0]["departure_date"]

            total_jamaah = len(jamaahs)

            required_tl = max(
                1,
                math.ceil(
                    total_jamaah /
                    Repair.MAX_JAMAAH_PER_TL
                )
            )

            selected_tls = []

            for tl in available_tls:

                conflict = False

                for used_date in tl_schedule[
                    tl["id"]
                ]:

                    try:

                        d1 = datetime.strptime(
                            departure_date,
                            "%Y-%m-%d"
                        )

                        d2 = datetime.strptime(
                            used_date,
                            "%Y-%m-%d"
                        )

                        diff_days = abs(
                            (d1 - d2).days
                        )

                        if diff_days <= 21:

                            conflict = True
                            break

                    except Exception:
                        pass

                if not conflict:

                    selected_tls.append(
                        tl
                    )

                if len(
                    selected_tls
                ) >= required_tl:

                    break

            if len(
                selected_tls
            ) < required_tl:

                remaining = required_tl - len(
                    selected_tls
                )

                selected_tls.extend(
                    available_tls[:remaining]
                )

            for tl in selected_tls:

                tl_schedule[
                    tl["id"]
                ].append(
                    departure_date
                )

            for index, gene in enumerate(
                jamaahs
            ):

                tl = selected_tls[
                    index % len(
                        selected_tls
                    )
                ]

                gene[
                    "team_leader_id"
                ] = tl["id"]

                gene[
                    "team_leader_name"
                ] = tl["name"]

                gene[
                    "team_leader_status"
                ] = tl["status"]

        # =====================================
        # REBALANCE MUTHOWIF
        # =====================================

        for departure_id, jamaahs in departure_groups.items():

            departure_date = jamaahs[0]["departure_date"]

            total_jamaah = len(jamaahs)

            required_muthowif = max(
                1,
                math.ceil(
                    total_jamaah /
                    Repair.MAX_JAMAAH_PER_MUTHOWIF
                )
            )

            selected_muthowifs = []

            for m in available_muthowifs:

                conflict = False

                for used_date in (
                    muthowif_schedule[
                        m["id"]
                    ]
                ):

                    try:

                        d1 = datetime.strptime(
                            departure_date,
                            "%Y-%m-%d"
                        )

                        d2 = datetime.strptime(
                            used_date,
                            "%Y-%m-%d"
                        )

                        diff_days = abs(
                            (d1 - d2).days
                        )

                        if diff_days <= 21:

                            conflict = True
                            break

                    except Exception:
                        pass

                if not conflict:

                    selected_muthowifs.append(
                        m
                    )

                if len(
                    selected_muthowifs
                ) >= required_muthowif:

                    break

            if len(
                selected_muthowifs
            ) < required_muthowif:

                remaining = (
                    required_muthowif
                    -
                    len(
                        selected_muthowifs
                    )
                )

                selected_muthowifs.extend(
                    available_muthowifs[
                        :remaining
                    ]
                )

            for m in selected_muthowifs:

                muthowif_schedule[
                    m["id"]
                ].append(
                    departure_date
                )

            for index, gene in enumerate(
                jamaahs
            ):

                m = selected_muthowifs[
                    index %
                    len(
                        selected_muthowifs
                    )
                ]

                gene[
                    "muthowif_id"
                ] = m["id"]

                gene[
                    "muthowif_name"
                ] = m["name"]

                gene[
                    "muthowif_status"
                ] = m["status"]

        return chromosome
"""Assignment 7, Question 3: changes in hive weight over time.

Reads the clean records, not the scored ones. Weight changes don't need risk
scores, so this module branches off the pipeline before hive.risk.

For each hive, in date order, every valid weight is compared with that hive's
previous valid weight. A missing weight is set aside, not treated as zero, so the
next valid weight is compared with the last weight that was actually measured.
"""
from hive.grouping import hive_ids, records_for_hive


def weight_changes(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Find each hive's weight change between consecutive valid weighings.

    Args:
        records: Clean inspection records, in any order.

    Returns:
        (changes, skipped):
            changes: one dict per comparison, with hive_id, previous_date,
                inspection_date, previous_weight, weight_lb, change_lb (negative
                means the hive lost weight) and days between the two weighings.
            skipped: the inspections that had no weight, so were not compared.
    """
    changes = []
    skipped = []

    for hive_id in hive_ids(records):
        previous = None  # this hive's last record that had a weight

        for record in records_for_hive(records, hive_id):
            weight = record["weight_lb"]

            # Missing weight: skip it, and leave previous alone, so the next valid
            # weight is compared with the last real one (never with zero)
            if weight is None:
                skipped.append({"hive_id": hive_id,
                                "inspection_date": record["inspection_date"]})
                continue

            if previous is not None:
                changes.append({
                    "hive_id": hive_id,
                    "previous_date": previous["inspection_date"],
                    "inspection_date": record["inspection_date"],
                    "previous_weight": previous["weight_lb"],
                    "weight_lb": weight,
                    # Weights are recorded to 0.1 lb; rounding removes float error
                    "change_lb": round(weight - previous["weight_lb"], 1),
                    # date - date gives a timedelta; .days is its whole-day count
                    "days": (record["inspection_date"] - previous["inspection_date"]).days,
                })

            previous = record

    return changes, skipped

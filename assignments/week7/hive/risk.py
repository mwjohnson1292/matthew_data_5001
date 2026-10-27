"""Assignment 6, Question 1: score each clean record for hive risk.

| Condition                                              | Points |
|--------------------------------------------------------|--------|
| mites is 8 or greater                                  | 3      |
| queen_seen is False                                    | 2      |
| weight fell 10 lb or more from the previous valid one  | 2      |
| temp_f is below 55 or above 95                         | 1      |

add_risk_fields is the entry point: it scores copies of the clean records in date
order within each hive, so "previous valid weight" always means that hive's last
known weight.
"""
from hive.grouping import hive_ids, records_for_hive

# Risk thresholds and points
MITE_THRESHOLD = 8
MITE_POINTS = 3
QUEEN_MISSING_POINTS = 2
WEIGHT_LOSS_THRESHOLD_LB = 10
WEIGHT_LOSS_POINTS = 2
TEMP_LOW_F = 55
TEMP_HIGH_F = 95
TEMP_POINTS = 1


def calculate_risk(record: dict, previous_weight: float | None) -> tuple[int, list[str]]:
    """Score one clean record against the risk table.

    Args:
        record: A clean inspection record.
        previous_weight: The hive's last valid weight, or None if there is none.

    Returns:
        (score, reasons): integer score and one reason string per condition met.

    Raises:
        ValueError: If the record is missing a field the score needs.
    """
    # Error handling 1 (Assignment 6, Q3): a missing field fails loudly instead of scoring 0
    try:
        mites = record["mites"]
        queen_seen = record["queen_seen"]
        weight = record["weight_lb"]
        temp = record["temp_f"]
    except KeyError as exc:
        raise ValueError(f"record is missing field {exc}") from exc

    score = 0
    reasons = []

    if mites >= MITE_THRESHOLD:
        score += MITE_POINTS
        reasons.append(f"mites {mites} >= {MITE_THRESHOLD}")

    if not queen_seen:
        score += QUEEN_MISSING_POINTS
        reasons.append("queen not seen")

    # No previous weight or no current weight: no weight points
    if previous_weight is not None and weight is not None:
        loss = round(previous_weight - weight, 1)  # weights are to 0.1 lb; avoids float error
        if loss >= WEIGHT_LOSS_THRESHOLD_LB:
            score += WEIGHT_LOSS_POINTS
            reasons.append(f"lost {loss} lb")

    # Missing temperature: no temp points
    if temp is not None and (temp < TEMP_LOW_F or temp > TEMP_HIGH_F):
        score += TEMP_POINTS
        reasons.append(f"temp {temp} outside {TEMP_LOW_F}-{TEMP_HIGH_F}")

    return score, reasons


def add_risk_fields(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Add risk_score and risk_reasons to copies of the clean records.

    Records are scored in date order within each hive, so previous_weight is always
    that hive's last valid weight. The input records are not changed.

    Returns:
        (scored, skipped): scored copies, and any records that could not be scored.
    """
    scored = []
    skipped = []

    for hive_id in hive_ids(records):
        previous_weight = None  # no previous weight at the start of each hive

        for record in records_for_hive(records, hive_id):
            # Error handling 2 (Assignment 6, Q3): skip one bad record, keep scoring the rest
            try:
                score, reasons = calculate_risk(record, previous_weight)
            except (TypeError, ValueError) as exc:
                skipped.append({"hive_id": hive_id, "inspection_date": record["inspection_date"],
                                "reason": str(exc)})
                continue

            scored_record = dict(record)  # a copy, so the clean record stays unchanged
            scored_record["risk_score"] = score
            scored_record["risk_reasons"] = reasons
            scored.append(scored_record)

            if record["weight_lb"] is not None:
                previous_weight = record["weight_lb"]

    return scored, skipped

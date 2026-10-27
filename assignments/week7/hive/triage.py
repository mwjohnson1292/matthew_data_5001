"""Assignment 7, Question 4: rank hives from most to least in need of attention.

A beekeeper has limited time, so the question is where to go first. Each hive is
ranked by the risk score at its latest inspection, because triage is about the
hive's state now. Ties go to the hive with more mites, the largest single risk
factor. The ranking is plain Python with no plotting, so it can be tested on its
own; q4_triage_chart.py draws it.
"""
from hive.grouping import hive_ids, records_for_hive
from hive.summary import risk_label


def rank_hives(scored: list[dict]) -> list[dict]:
    """Rank hives from most to least urgent.

    Args:
        scored: Scored inspection records (from add_risk_fields), in any order.

    Returns:
        One dict per hive, most urgent first, with hive_id, latest_date,
        risk_score, risk_label, mites and risk_reasons from the hive's latest
        inspection, plus previous_score (None when the hive has only one).
    """
    ranked = []
    for hive_id in hive_ids(scored):
        inspections = records_for_hive(scored, hive_id)  # oldest to newest
        latest = inspections[-1]
        previous = inspections[-2] if len(inspections) > 1 else None
        ranked.append({
            "hive_id": hive_id,
            "latest_date": latest["inspection_date"],
            "risk_score": latest["risk_score"],
            "risk_label": risk_label(latest["risk_score"]),
            "previous_score": previous["risk_score"] if previous is not None else None,
            "mites": latest["mites"],
            "risk_reasons": latest["risk_reasons"],
        })

    # Highest score first; among equal scores, more mites first.
    # A tuple key sorts by its first item, then uses the second to break ties.
    ranked.sort(key=lambda hive: (hive["risk_score"], hive["mites"]), reverse=True)
    return ranked

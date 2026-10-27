"""Group records by hive and put each hive's records in date order.

Three modules need this (risk, summary and weights), so it lives in its own
module instead of inside any one of them. Every module that groups by hive
imports it from here.
"""


def hive_ids(records: list[dict]) -> list[str]:
    """Unique hive IDs in the records, sorted (H-01, H-02, ...)."""
    return sorted({record["hive_id"] for record in records})


def records_for_hive(records: list[dict], hive_id: str) -> list[dict]:
    """Return one hive's records sorted oldest to newest (input order is not trusted)."""
    matches = [record for record in records if record["hive_id"] == hive_id]
    return sorted(matches, key=lambda record: record["inspection_date"])

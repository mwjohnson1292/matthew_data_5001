"""Assignment 6, Questions 2 and 4: summarize one hive's scored records.

summarize_hive (Q2) builds the summary with four helper functions. The Hive class
(Q4) builds the same summary as an object, and Assignment 6 tested that the two
always match.

Decisions carried over from Assignment 6:
    Empty hive: the same keys, with inspection_count 0 and every other field None.
        Not 0, because 0 mites or a risk of 0 would look like a real, healthy hive.
    latest_weight: the most recent weight that is not missing.
"""
from hive.grouping import records_for_hive

REVIEW_MIN_SCORE = 3
URGENT_MIN_SCORE = 6
SUMMARY_FIELDS = ["hive_id", "inspection_count", "first_date", "last_date", "average_temp",
                  "latest_weight", "total_mites", "maximum_risk", "risk_label"]


def check_hive_id(hive_id) -> None:
    """Raise ValueError unless hive_id is "H-" followed by two digits."""
    # Error handling 3 (Assignment 6, Q3): a typo is an error, not an empty hive
    if not (isinstance(hive_id, str) and len(hive_id) == 4
            and hive_id.startswith("H-") and hive_id[2:].isdigit()):
        raise ValueError(f"Invalid hive_id: {hive_id!r}")


def average_ignoring_missing(values: list) -> float | None:
    """Mean of the values that are not None; None if every value is missing."""
    present = [value for value in values if value is not None]
    if not present:
        return None
    return sum(present) / len(present)


def latest_known(values: list):
    """Last value that is not None in an oldest-to-newest list; None if all are missing."""
    for value in reversed(values):
        if value is not None:
            return value
    return None


def risk_label(score: int) -> str:
    """low for 0-2, review for 3-5, urgent for 6 or greater."""
    if score >= URGENT_MIN_SCORE:
        return "urgent"
    if score >= REVIEW_MIN_SCORE:
        return "review"
    return "low"


def summarize_hive(records: list[dict], hive_id: str) -> dict:
    """Summarize one hive's scored inspection records.

    Records can arrive in any order; they are sorted by date first.

    Returns:
        A dict with every key in SUMMARY_FIELDS. A hive with no records returns
        inspection_count 0 and None for every other field.

    Raises:
        ValueError: If hive_id is not "H-" followed by two digits.
    """
    check_hive_id(hive_id)
    hive = records_for_hive(records, hive_id)

    if not hive:
        summary = dict.fromkeys(SUMMARY_FIELDS)  # every field None
        summary.update(hive_id=hive_id, inspection_count=0)
        return summary

    maximum_risk = max(record["risk_score"] for record in hive)
    return {
        "hive_id": hive_id,
        "inspection_count": len(hive),
        "first_date": hive[0]["inspection_date"],
        "last_date": hive[-1]["inspection_date"],
        "average_temp": average_ignoring_missing([record["temp_f"] for record in hive]),
        "latest_weight": latest_known([record["weight_lb"] for record in hive]),
        "total_mites": sum(record["mites"] for record in hive),
        "maximum_risk": maximum_risk,
        "risk_label": risk_label(maximum_risk),
    }


class Hive:
    """One hive and its scored inspection records.

    Why a class: summarize_hive and its helpers all start from the same data, one
    hive's records sorted by date. A Hive sorts once when it is created and keeps
    the records, so each method reads self.records instead of filtering again.
    """

    def __init__(self, hive_id: str, records: list[dict]):
        check_hive_id(hive_id)
        self.hive_id = hive_id
        self.records = sorted(records, key=lambda record: record["inspection_date"])

    @classmethod
    def from_records(cls, records: list[dict], hive_id: str) -> "Hive":
        """Build a Hive from the full apiary list, keeping only this hive's records."""
        return cls(hive_id, [record for record in records if record["hive_id"] == hive_id])

    @staticmethod
    def label(score: int) -> str:
        """Same labels as risk_label, which defines the bands once for the whole module."""
        return risk_label(score)

    def maximum_risk(self) -> int | None:
        """Highest risk score for this hive; None if it has no records."""
        if not self.records:
            return None
        return max(record["risk_score"] for record in self.records)

    def summary(self) -> dict:
        """Same dictionary as summarize_hive, built from this hive's records."""
        if not self.records:
            summary = dict.fromkeys(SUMMARY_FIELDS)
            summary.update(hive_id=self.hive_id, inspection_count=0)
            return summary

        highest = self.maximum_risk()
        return {
            "hive_id": self.hive_id,
            "inspection_count": len(self.records),
            "first_date": self.records[0]["inspection_date"],
            "last_date": self.records[-1]["inspection_date"],
            "average_temp": average_ignoring_missing([r["temp_f"] for r in self.records]),
            "latest_weight": latest_known([r["weight_lb"] for r in self.records]),
            "total_mites": sum(record["mites"] for record in self.records),
            "maximum_risk": highest,
            "risk_label": Hive.label(highest),
        }

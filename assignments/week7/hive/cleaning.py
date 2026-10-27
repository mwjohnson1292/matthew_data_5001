"""Assignment 5 cleaning: turn raw inspection records into clean, typed records.

clean_records is the entry point. It runs normalize_record on every raw record,
which uses parse_date and to_bool, and then drops duplicate inspections.
"""
from datetime import datetime


def parse_date(raw_date):
    """Parse YYYY-MM-DD or MM/DD/YYYY into a date; raise ValueError if invalid."""
    try:
        if "-" in raw_date:
            return datetime.strptime(raw_date, "%Y-%m-%d").date()
        return datetime.strptime(raw_date, "%m/%d/%Y").date()
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid inspection_date: {raw_date}") from exc


def to_bool(value):
    """Convert "yes"/"no" to True/False; keep booleans; raise ValueError otherwise."""
    if value == "yes":
        return True
    if value == "no":
        return False
    if isinstance(value, bool):
        return value
    raise ValueError(f"Invalid queen_seen: {value}")


def normalize_record(record: dict) -> tuple[dict | None, str]:
    """Return (clean_record, "") if valid, or (None, reason) if rejected."""
    try:
        hive_id = str(record.get("hive_id", "")).strip().upper()
        if len(hive_id) != 4 or not hive_id.startswith("H-") or not hive_id[2:].isdigit():
            raise ValueError(f"Invalid hive_id: {hive_id}")

        inspection_date = parse_date(record.get("inspection_date"))

        temp_f = record.get("temp_f")
        if temp_f is not None:
            temp_f = float(str(temp_f).removesuffix("F"))
            if temp_f < -20 or temp_f > 130:
                raise ValueError(f"temp_f out of range: {temp_f}")

        try:
            weight_lb = float(record.get("weight_lb"))
        except (TypeError, ValueError):
            weight_lb = None
        if weight_lb is not None and weight_lb < 0:
            raise ValueError(f"weight_lb cannot be negative: {weight_lb}")

        mites = int(record.get("mites"))
        if mites < 0:
            raise ValueError(f"mites cannot be negative: {mites}")

        queen_seen = to_bool(record.get("queen_seen"))

        notes = record.get("notes")
        if notes is None:
            notes = ""

    except (TypeError, ValueError) as exc:
        return None, str(exc)

    clean = {
        "hive_id": hive_id,
        "inspection_date": inspection_date,
        "temp_f": temp_f,
        "weight_lb": weight_lb,
        "mites": mites,
        "queen_seen": queen_seen,
        "notes": notes,
    }
    return clean, ""


def clean_records(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Normalize every record, then remove duplicates by hive_id + inspection_date."""
    clean = []
    rejected = []
    seen = set()

    for index, record in enumerate(records):
        result, reason = normalize_record(record)
        if result is None:
            rejected.append({"source_index": index, "hive_id": record.get("hive_id"),
                             "reason": reason})
            continue

        key = (result["hive_id"], result["inspection_date"])
        if key in seen:
            rejected.append({"source_index": index, "hive_id": result["hive_id"],
                             "reason": "duplicate inspection"})
            continue

        seen.add(key)
        clean.append(result)

    return clean, rejected

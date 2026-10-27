"""Run the hive pipeline in one call: raw -> clean -> scored.

Questions 2, 3 and 4 all start from the pipeline's output, so the order of the
stages is written here once. It plays the role an orchestration step plays in an
ETL pipeline: run each stage in order and hand back the results.
"""
from collections import namedtuple

from hive.cleaning import clean_records
from hive.data import RAW_INSPECTIONS
from hive.risk import add_risk_fields

# A tuple whose parts have names: result.scored instead of result[2]
PipelineResult = namedtuple("PipelineResult", ["clean", "rejected", "scored", "skipped"])


def run_pipeline(raw_records: list[dict] | None = None) -> PipelineResult:
    """Clean and score inspection records.

    Args:
        raw_records: Raw inspection dicts. Defaults to the starter data in hive.data.

    Returns:
        PipelineResult with the clean, rejected, scored and skipped lists.
    """
    # None as the default, not RAW_INSPECTIONS, so the default is chosen at call time
    if raw_records is None:
        raw_records = RAW_INSPECTIONS
    clean, rejected = clean_records(raw_records)
    scored, skipped = add_risk_fields(clean)
    return PipelineResult(clean, rejected, scored, skipped)

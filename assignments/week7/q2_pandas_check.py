"""Assignment 7, Question 2: verify the core Python pipeline with pandas.

The hive package stays the source of truth. pandas reads the same scored records
a second way, and assert statements check that the two agree on the row count,
the number of hives and the total mites. It is the same idea as a reconciliation
check in an ETL pipeline: compute a number two ways and require them to match.

Why matching isn't proof: Two implementations agreeing raises my confidence,
because a mistake would have to show up the same way in both to slip through,
but it doesn't prove either one is correct: both read the same cleaned records
and follow my same reading of the rules, so an error in the cleaning or in how I
read the spec would appear in both and they would still agree.

What the output shows: all four inspections that need attention have the same
two problems together, 8 or more mites and no queen seen. H-06 is the only hive
flagged on both visits, and its score rose from 6 to 8 when it also lost 10.6 lb,
so it is getting worse, not just staying bad.

Run with:
    python q2_pandas_check.py
This file must stay next to the hive/ folder: Python looks for hive in the
folder that holds the script, not the folder you run it from.
"""
import pandas as pd

from hive.grouping import hive_ids
from hive.pipeline import run_pipeline
from hive.summary import REVIEW_MIN_SCORE, summarize_hive

# The columns the prompt asks to keep for inspections needing attention
ATTENTION_COLUMNS = ["hive_id", "inspection_date", "mites", "risk_score", "risk_reasons"]


def core_totals(scored: list[dict]) -> dict:
    """Row count, unique hives and total mites, from the core Python functions.

    Total mites comes from summarize_hive, so pandas is checked against the
    pipeline's own summaries, not against new code written just for this check.
    """
    ids = hive_ids(scored)
    return {
        "rows": len(scored),
        "hives": len(ids),
        "mites": sum(summarize_hive(scored, hive_id)["total_mites"] for hive_id in ids),
    }


def pandas_totals(df: pd.DataFrame) -> dict:
    """The same three numbers, computed independently with pandas."""
    return {
        "rows": len(df),
        "hives": df["hive_id"].nunique(),
        "mites": int(df["mites"].sum()),
    }


def main():
    """Build the DataFrame, verify it against the core pipeline, list inspections to act on."""
    scored = run_pipeline().scored

    # ---- One row per scored inspection ----
    df = pd.DataFrame(scored)
    print("dtypes as loaded:")
    print(df.dtypes, "\n")

    # Python date objects load as a generic object column; convert to pandas datetime
    # .assign returns a new DataFrame instead of changing df in place
    df = df.assign(inspection_date=pd.to_datetime(df["inspection_date"]))
    print("dtypes after converting inspection_date:")
    print(df.dtypes, "\n")

    # ---- Missing values in every column ----
    print("Missing values per column:")
    print(df.isna().sum(), "\n")

    # ---- Verify pandas against the core pipeline ----
    core = core_totals(scored)
    check = pandas_totals(df)
    assert check["rows"] == core["rows"], "row count differs"
    assert check["hives"] == core["hives"], "unique hive count differs"
    assert check["mites"] == core["mites"], "total mites differs"
    print("pandas matches the core pipeline:", core, "\n")

    # ---- Inspections needing attention: risk_score of 3 or more (the review band) ----
    df = df.assign(needs_attention=df["risk_score"] >= REVIEW_MIN_SCORE)
    attention = df.loc[df["needs_attention"], ATTENTION_COLUMNS]
    print(f"Inspections needing attention ({len(attention)} of {len(df)}):")
    print(attention.to_string(index=False))


# Runs only when this file is executed directly, not when another file imports it
if __name__ == "__main__":
    main()

"""Assignment 7, Question 1: the Assignment 6 notebook, rebuilt as a package and a script.

Question: Convert your ipynb files to py files. Use at least one module and import
accordingly. Does a module make sense here? Why?

Answer: Yes. In Assignment 6 I had to paste Assignment 5's data and cleaning
functions into a setup cell, because a notebook can't be imported. Here the modules
follow the stages of the pipeline (data -> cleaning -> risk -> summary). Every
script imports the same code instead of copying it (code reuse), and each module
has one job, so a fix made in one module reaches every script and names in one
module can't clash with another's (partitioning). It's the same reason a team's
scripts should share one authentication module and one config module instead of
repeating that code in each one: define it in one place, and it flows out to
everything that imports it.

Layout:
    hive/            the package: definitions only, so importing it runs nothing
    q1_run_pipeline  this script: runs the Assignment 6 pipeline and its tests

Run with:
    python q1_run_pipeline.py
This file must stay next to the hive/ folder: Python looks for hive in the
folder that holds the script, not the folder you run it from.

The output matches the Assignment 6 notebook line for line. The move into modules
changed where the code lives, not what it does.
"""
from datetime import date

from hive.grouping import hive_ids
from hive.pipeline import run_pipeline
from hive.risk import add_risk_fields, calculate_risk
from hive.summary import SUMMARY_FIELDS, Hive, risk_label, summarize_hive


# ---- Assignment 6, Question 1: risk score tests ----

def make_record(**changes):
    """Build a zero-risk test record; keyword arguments override fields."""
    record = {"hive_id": "H-99", "inspection_date": date(2026, 9, 1), "temp_f": 75.0,
              "weight_lb": 150.0, "mites": 0, "queen_seen": True, "notes": ""}
    record.update(changes)
    return record


def test_risk_boundaries():
    """Boundary tests for each threshold, plus the missing-weight rules."""
    # Mites: 8 scores, 7 does not
    assert calculate_risk(make_record(mites=8), None) == (3, ["mites 8 >= 8"])
    assert calculate_risk(make_record(mites=7), None) == (0, [])

    # Weight: exactly 10 lb lost scores, 9.9 does not
    assert calculate_risk(make_record(weight_lb=140.0), 150.0) == (2, ["lost 10.0 lb"])
    assert calculate_risk(make_record(weight_lb=140.1), 150.0) == (0, [])
    # 128.2 - 118.2 is 9.99999... in floating point; rounding keeps it at 10
    assert calculate_risk(make_record(weight_lb=118.2), 128.2)[0] == 2

    # Weight: no previous weight, or a missing current weight, earns no points
    assert calculate_risk(make_record(weight_lb=100.0), None) == (0, [])
    assert calculate_risk(make_record(weight_lb=None), 150.0) == (0, [])

    # Temperature: 95 is not above 95; 95.1 is
    assert calculate_risk(make_record(temp_f=95.0), None) == (0, [])
    assert calculate_risk(make_record(temp_f=95.1), None)[0] == 1
    assert calculate_risk(make_record(temp_f=None), None) == (0, [])

    print("All risk boundary tests passed")


def print_scored(records):
    """Print hive, date, score, and reasons for each scored record."""
    for record in records:
        print(record["hive_id"], record["inspection_date"], record["risk_score"],
              record["risk_reasons"])


# ---- Assignment 6, Question 2: summary tests ----

def test_summaries(scored):
    """Unsorted input, missing values, risk labels, and the empty hive."""
    unsorted = list(reversed(scored))  # newest first, on purpose

    h06 = summarize_hive(unsorted, "H-06")
    assert h06["first_date"] == date(2026, 8, 6)
    assert h06["last_date"] == date(2026, 8, 20)
    assert h06["maximum_risk"] == 8 and h06["risk_label"] == "urgent"

    h03 = summarize_hive(unsorted, "H-03")
    assert h03["average_temp"] == 96.0      # the missing temp is ignored
    assert h03["latest_weight"] == 130.0    # the missing latest weight is skipped

    assert [risk_label(s) for s in (0, 2, 3, 5, 6)] == ["low", "low", "review", "review", "urgent"]

    empty = summarize_hive(scored, "H-07")
    assert empty["inspection_count"] == 0
    assert all(empty[field] is None for field in SUMMARY_FIELDS[2:])

    print("All summary tests passed")


def print_summaries(records):
    """Print the summary for every hive in the records."""
    for hive_id in hive_ids(records):
        print(summarize_hive(records, hive_id))


# ---- Assignment 6, Question 3: error handling ----

def demo_error_handling(scored):
    """Trigger each of the three error-handling cases."""
    # 1. calculate_risk: a record missing a field
    broken = make_record()
    del broken["mites"]
    try:
        calculate_risk(broken, None)
    except ValueError as exc:
        print("1.", exc)

    # 2. add_risk_fields: one record with text where a number belongs
    bad = make_record(inspection_date=date(2026, 9, 2), mites="many")
    scored_demo, skipped = add_risk_fields([make_record(), bad])
    print("2.", len(scored_demo), "scored |", skipped)

    # 3. summarize_hive: a malformed hive_id
    try:
        summarize_hive(scored, "H6")
    except ValueError as exc:
        print("3.", exc)


# ---- Assignment 6, Question 4: the Hive class ----

def test_hive_class(scored):
    """The class must produce the same summary as summarize_hive, including empty hives."""
    for hive_id in ["H-01", "H-02", "H-03", "H-04", "H-05", "H-06", "H-07"]:
        assert Hive.from_records(scored, hive_id).summary() == summarize_hive(scored, hive_id)
    print("Hive class matches summarize_hive for every hive")
    print(Hive.from_records(scored, "H-06").summary())


# ---- Run everything, in the notebook's order ----

def main():
    """Clean, score, summarize, and test, in the same order as the Assignment 6 notebook."""
    result = run_pipeline()
    print(len(result.clean), "clean |", len(result.rejected), "rejected")

    test_risk_boundaries()

    print_scored(result.scored)
    print("Skipped:", result.skipped)
    print("Clean records unchanged:", all("risk_score" not in r for r in result.clean))

    test_summaries(result.scored)
    print_summaries(result.scored)
    demo_error_handling(result.scored)
    test_hive_class(result.scored)


# Runs only when this file is executed directly, not when another file imports it
if __name__ == "__main__":
    main()

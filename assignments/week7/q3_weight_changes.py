"""Assignment 7, Question 3: detect changes in hive weight over time.

Question: Write a function that identifies changes in hive weight over time using
your cleaned inspection records. It must group inspections by hive_id and order
each hive's inspections by date, skip inspections with missing weights without
treating them as zero, and compare each valid weight with the previous valid
weight for that same hive.

Answer: weight_changes in hive/weights.py. This script tests it, then runs it on
the clean records from the pipeline.

Why the tests use made-up records: the real data never has a valid weight, then a
missing one, then a valid one again. H-03's missing weight is its last inspection
and H-05's is its first. That middle gap is the case "previous valid weight"
exists for, so the tests build it directly.

What the output shows: every change that could be measured is a loss, and all
three cover the same 14 days, so they compare directly. H-06 lost the most,
10.6 lb, the same loss that raised its risk score in Assignment 6. H-03, H-04 and
H-05 each have only one valid weight, so their change is unknown, not zero: no
change measured is not the same as no change.

Run with:
    python q3_weight_changes.py
This file must stay next to the hive/ folder: Python looks for hive in the
folder that holds the script, not the folder you run it from.
"""
from datetime import date

from hive.pipeline import run_pipeline
from hive.weights import weight_changes


# ---- Tests ----

def make_record(hive_id, day, weight):
    """A minimal clean record with only the fields weight_changes reads."""
    return {"hive_id": hive_id, "inspection_date": date(2026, 9, day), "weight_lb": weight}


def test_weight_changes():
    """The three required behaviors, plus the floating-point trap."""
    # A missing weight in the middle: day 15 is compared with day 1.
    # Treating the gap as zero would have produced two changes, -150 and +140.
    changes, skipped = weight_changes([
        make_record("H-10", 1, 150.0),
        make_record("H-10", 8, None),
        make_record("H-10", 15, 140.0),
    ])
    assert [change["change_lb"] for change in changes] == [-10.0]
    assert changes[0]["previous_date"] == date(2026, 9, 1)
    assert changes[0]["days"] == 14
    assert skipped == [{"hive_id": "H-10", "inspection_date": date(2026, 9, 8)}]

    # A missing weight first or last leaves only one valid weight: nothing to compare
    changes, skipped = weight_changes([make_record("H-11", 1, None),
                                       make_record("H-11", 8, 120.0)])
    assert not changes and len(skipped) == 1  # an empty list counts as False
    changes, skipped = weight_changes([make_record("H-12", 1, 120.0),
                                       make_record("H-12", 8, None)])
    assert not changes and len(skipped) == 1  # an empty list counts as False

    # Out-of-order input is put in date order first
    changes, _ = weight_changes([make_record("H-13", 15, 130.0),
                                 make_record("H-13", 1, 135.0)])
    assert changes[0]["change_lb"] == -5.0
    assert changes[0]["previous_date"] == date(2026, 9, 1)

    # Two different hives are never compared with each other
    changes, _ = weight_changes([make_record("H-14", 1, 100.0),
                                 make_record("H-15", 8, 200.0)])
    assert not changes

    # Floating point: 118.2 - 128.2 is -9.99999... until it is rounded
    changes, _ = weight_changes([make_record("H-16", 1, 128.2),
                                 make_record("H-16", 8, 118.2)])
    assert changes[0]["change_lb"] == -10.0

    print("All weight change tests passed")


# ---- Results on the real data ----

def print_changes(changes, skipped):
    """Print one line per weight change, then the inspections that were skipped."""
    print(f"Weight changes ({len(changes)}):")
    for change in changes:
        print(f"  {change['hive_id']}  {change['previous_date']} -> {change['inspection_date']}"
              f"  {change['previous_weight']:.1f} -> {change['weight_lb']:.1f} lb"
              f"  change {change['change_lb']:+.1f} lb over {change['days']} days")

    print(f"Skipped, no weight recorded ({len(skipped)}):")
    for record in skipped:
        print(f"  {record['hive_id']}  {record['inspection_date']}")


def main():
    """Test weight_changes, then run it on the clean inspection records."""
    test_weight_changes()
    changes, skipped = weight_changes(run_pipeline().clean)
    print_changes(changes, skipped)


# Runs only when this file is executed directly, not when another file imports it
if __name__ == "__main__":
    main()

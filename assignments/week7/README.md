# Assignment 7: Modules and Packages

An extension of Assignment 6. The Assignment 6 notebook
(`assignments/week6/homework_6_answers.ipynb`) was converted to a Python script
with `jupyter nbconvert --to script`, then split into a package, `hive/`, plus
one script per question.

## Files

| File | What it holds |
|---|---|
| `hive/__init__.py` | Marks `hive/` as a package and lists its modules |
| `hive/data.py` | The starter inspection records (Assignment 5) |
| `hive/cleaning.py` | Cleaning: `clean_records` and its helpers (Assignment 5) |
| `hive/grouping.py` | `hive_ids`, `records_for_hive`: group by hive, order by date |
| `hive/risk.py` | Risk scoring: `calculate_risk`, `add_risk_fields` (Assignment 6, Q1) |
| `hive/summary.py` | `summarize_hive` and the `Hive` class (Assignment 6, Q2 and Q4) |
| `hive/pipeline.py` | `run_pipeline`: runs cleaning, then scoring, in one call |
| `hive/weights.py` | `weight_changes` (Question 3) |
| `hive/triage.py` | `rank_hives` (Question 4) |
| `q1_run_pipeline.py` | Question 1: reruns Assignment 6 from the package, with its tests |
| `q2_pandas_check.py` | Question 2: pandas verification |
| `q3_weight_changes.py` | Question 3: tests and results for `weight_changes` |
| `q4_triage_chart.py` | Question 4: the triage chart |
| `q4_triage_chart.png` | The chart that `q4_triage_chart.py` saves |
| `AI_COLLABORATION.md` | How GenAI was used, and who did what |

Each question's answer, explanation and interpretation of results is in the
docstring at the top of its script.

## How to run

Python 3.11 or newer, with pandas and matplotlib (both in the repo's
`requirements.txt`). Tested with pandas 2.2.3 and 3.0.3.

```
python q1_run_pipeline.py
python q2_pandas_check.py
python q3_weight_changes.py
python q4_triage_chart.py
```

Keep the scripts next to the `hive/` folder. Python looks for `hive` in the
folder that holds the script being run, not the folder you run it from.

## Results

- **Q1:** a module makes sense here: Assignment 6 had to paste Assignment 5's
  code into a setup cell, and now every script imports it instead. The Q1 script's
  output matches the Assignment 6 notebook line for line.
- **Q2:** pandas and the core pipeline agree: 11 inspections, 6 hives, 61 mites.
  4 inspections need attention.
- **Q3:** three weight changes could be measured, all losses over 14 days:
  H-01 −5.5 lb, H-02 −3.8 lb, H-06 −10.6 lb. Two inspections had no weight and
  were skipped, not treated as zero.
- **Q4:** visit H-06 first. It is urgent and scored worse than at its last
  inspection; H-03 and H-01 come next.

## Linting

From this folder, with the repo's `.pylintrc`:

```
pylint hive q1_run_pipeline.py q2_pandas_check.py q3_weight_changes.py q4_triage_chart.py --rcfile=../../.pylintrc
```

Result: **10.00/10**.

## AI use

GenAI was used with attribution, as the assignment allows. See
`AI_COLLABORATION.md` for how it was used and who did what.

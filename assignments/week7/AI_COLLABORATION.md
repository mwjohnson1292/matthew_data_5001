# AI Collaboration Log: Assignment 7

This assignment allows GenAI tools with attribution. This log is that
attribution: what the AI did, what I did, and how the work was checked.

**Tool:** Claude (Anthropic), through Claude Code, in one working session on
October 26, 2026.

**How we worked:** Claude wrote the code and the first drafts of the written
answers. I then reviewed every file with it, section by section and line by line,
asking questions and changing things as we went. Claude laid out design options
with a recommendation, and I made the calls. Claude ran every check and showed me
the output.

## What came from me

**Ideas**

- The real-world example in the Q1 answer. My team's scripts at work each repeat
  the same authentication code. One shared authentication module, and one shared
  config module, would define each thing once and let it flow out to every script.
- The story for Q4: rank the hives from most to least urgent, so a beekeeper can
  act first where it's needed most.
- Leaving the beekeeper's notes out of the Q4 chart, because they're too
  subjective for a triage ranking.

**Choices between options Claude laid out**

- A package instead of a single module.
- Explicit imports, which is how my team works at my job.
- Moving the grouping helpers into their own module once three modules needed them.
- Having `Hive.label` call `risk_label`, so the risk bands are defined once.
- `.assign` for new DataFrame columns.
- A static Python chart instead of Tableau, ranked by each hive's latest risk score.

## Connections to my own work

I asked for every concept to be tied to work I've already built. I made the first
connections, to my team's shared scripts at work and to my own data pipelines,
and Claude then found the matching code in my pipelines:

- **Packages and modules:** my data pipelines are organized the same way, as a
  package of shared modules (extract, transform, models) plus one script that
  runs them in order. `run_pipeline` plays the role of that orchestration step.
- **Pipeline stages:** data, cleaning, risk and summary mirror the raw, staging
  and reporting layers my pipelines load into a database. The difference is that
  mine save each stage, so one stage can be rerun from saved data. This
  assignment keeps everything in memory.
- **Shared config and authentication:** my pipelines already have one settings
  module (its docstring calls it the "single source of truth") and one
  authentication module that the rest of the code imports. That is the Q1
  example, already in practice.
- **`__init__.py`:** one of my own packages has no `__init__.py` and still
  imports, the Python 3.3+ behavior covered in the review.
- **Default arguments:** one of my pipelines writes `value or default`, which is
  safe for a date but would swap an empty list for the default. That is why
  `run_pipeline` checks `is None` instead.
- **Q2's verification:** my pipelines run the same kind of check. They recompute
  a daily total from the individual entries and require it to match the source's
  own total. That check is stronger than Q2's, because the source's totals never
  pass through my cleaning code.
- **Q3's previous valid weight:** in SQL this is `LAG()` over a window partitioned
  by hive and ordered by date, after filtering out the missing weights. One of my
  pipelines has a comment planning exactly that change.
- **Q4's split between ranking and drawing:** the same split as in my dashboard
  work. Build the data first, then the view that reads it.

## Question by question

### Q1: Modules

- `jupyter nbconvert` turned the Assignment 6 notebook into one script. Importing
  a single function from that script re-ran the whole assignment, because
  importing a file runs it from top to bottom. That is the case for modules:
  definitions go in modules, and the code that runs goes in scripts.
- The `hive/` package splits the code by pipeline stage: data, cleaning, risk,
  summary. While reviewing it, I connected the layout to how my team's scripts
  share logging, config, argument and export-folder code at work, which led to
  the authentication example.
- The review found one duplicate: `Hive.label` repeated `risk_label`. We fixed it.
- Check: the Q1 script's output matches the Assignment 6 notebook line for line.

### Q2: pandas verification

- pandas recomputes the row count, unique hives and total mites from the
  DataFrame, and three `assert` statements require them to match the core
  pipeline.
- Under pandas 2.2.3 on Python 3.14, adding a column raised a chained-assignment
  warning. The same code on Python 3.12 gave no warning, so it was a false alarm
  from that version pairing. I chose `.assign`, which runs without warnings on both.
- The example behind the one-sentence answer: cleaning turns a mite count of 8.7
  into 8, so pandas and the core pipeline would agree and both be wrong.

### Q3: Weight changes

- The real data never has a valid weight, then a missing one, then a valid one
  again, which is the case the "previous valid weight" rule exists for. The tests
  build that case with made-up records.
- Check: a deliberately broken copy that treats missing weights as zero fails
  the tests.

### Q4: Triage chart

- `rank_hives` ranks each hive by its latest risk score, with ties going to the
  hive with more mites. matplotlib draws the ranking.
- Claude rendered the chart and looked at it before I did. That caught two
  layout problems, threshold lines crossing their labels and a score crowding the
  text beside it, and both were fixed.

## Concepts covered in the review

Why importing a file runs it; how Python finds a package (`sys.path` starts at
the script's folder); `__init__.py`; named tuples; the mutable default argument
trap; `is None` versus truthiness (a 0°F reading is data, not missing);
floating-point rounding at the 10 lb line; `and`/`or` precedence; `sorted()`
versus `.sort()`; why a tuple can go in a set and a list can't; `assert` and
`python -O`; sorting with a tuple key.

## Corrections along the way

- One of Claude's docstrings said to run the scripts "from this folder." Testing
  showed they run from anywhere, as long as they stay next to `hive/`. Fixed.
- Installing matplotlib upgraded numpy and broke pandas in the linting
  environment. The earlier numpy was restored, and every script was re-checked.

## Final checks

- pylint: 10.00/10 on every file.
- All four scripts run on pandas 2.2.3 and 3.0.3.

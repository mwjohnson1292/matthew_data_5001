# AI Collaboration Log: Assignment 9

This assignment allows GenAI tools with attribution. This log is that attribution.

**Tool:** Claude (Anthropic), through Claude Code, November 9, 2026.

## How we worked

This time I designed and Claude built. For each question I set the direction: the preprocessing
rules, the story and the charts I wanted, and the question for the ANOVA. Claude turned that into
code, laid out options with a recommendation wherever my design left a choice open, and ran every
check. I reviewed every result and chart as it was built, asked questions until the statistics
made sense to me (one-hot encoding and multicollinearity, and what price per horsepower shows),
and made the final calls.

## What came from me

- **The preprocessing rules:**
  - numbers stored as text become numbers, and `?` becomes null;
  - all text is lowercase with no leading or trailing spaces;
  - column names are lowercase_snake_case, and `make` is in Title Case;
  - cylinders and doors stay nominal text;
  - outliers are determined statistically, and only values stored wrong are excluded;
  - one-hot encoding is used where it fits.
- **Origin as the story** that ties every chart together, shown in one consistent color, and the
  order of the charts from simple to complex.
- **The five questions the charts answer:** who makes the cars, price by make, engine size and
  fuel economy, cylinders and turbo against horsepower, and fuel type against fuel economy.
- **The idea behind Question 3:** European cars are pricier and more powerful, so is their price
  premium just paying for power?
- **In my own words:**
  - The four definitions. Claude added the opening "X is ..." phrase to each, which I kept.
  - The five chart summaries and the reasoning for checking outliers statistically.
  - The conclusion. Claude suggested three additions, which I accepted: the decision on the null
    hypothesis, the per-horsepower units, and naming both groups the premium is measured against.
- **My choices among Claude's options:**
  - the automobile dataset;
  - three origin regions instead of domestic vs. foreign;
  - price per horsepower for the ANOVA;
  - fixing the two misspelled makes;
  - dropping highway mpg for multicollinearity;
  - a standardized price column;
  - checking values against the documented ranges.

## What came from Claude

- **The code and the README.**
- **The chart designs:** one square per car, the dot strips, fuel use in gallons per 100 miles,
  the dumbbell chart, and a color palette checked for colorblind readers.
- **What it noticed in the data:** every car in it is an import, the two misspelled makes, and
  the rotary engines listed as "two" cylinders.
- **The statistics plan:** Levene's test, then Welch's ANOVA, Kruskal-Wallis and the
  Games-Howell follow-up.

## How the work was checked

- The notebook runs from top to bottom in a fresh kernel with no errors.
- pylint scores 10.00/10 with the repo's `.pylintrc`.
- The range check was tested with a planted error (horsepower 1110), and it caught it.
- The hypotheses were written before any test was run.
- Claude rendered and reviewed every chart. It fixed the problems it found: gridlines drawn
  through the squares, a missing axis tick, and overcrowded dots.

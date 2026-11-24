# AI Collaboration Log: Assignment 10

This assignment allows GenAI tools with attribution. This log is that attribution.

**Tool:** Claude (Anthropic), through Claude Code, November 23, 2026.

## How we worked

I designed and Claude built. I steered the analysis, making the choices below, Claude wrote 
the code and laid out options with a recommendation where a choice was open. We then 
walked through the notebook together, function by function, until I could explain each part, 
and I cut it down to what the assignment asks for.

## What came from me

- **My choices:** the Ames Housing dataset; above or below the median price
  as the logistic regression target; correlation plus cross validation for feature selection; and
  which sections to keep or cut.
- **The four written answers**, in my own words. My Question 1 answer reuses part of a summary
  sentence Claude drafted. Claude checked each answer against the question and the results and
  pointed out gaps and one wrong definition (precision vs. recall), which I fixed myself.

## What came from Claude

- **The code, the charts and this log.**
- **What it noticed in the data:** the file writes "NA" to mean "the home has none," which
  pandas' default reading would turn into missing values; a garage dated 2207; a remodel dated
  before its house was built.
- **The feature selection method in detail:** the 0.5 and 0.8 correlation cutoffs and the
  cross-validation comparison.

## How the work was checked

- The notebook runs from top to bottom in a fresh kernel with no errors.
- pylint scores 10.00/10 (max line length 100).
- Both models are scored on 20% of homes held out from training and from every preparation step.

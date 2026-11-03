# AI Collaboration Log: Assignment 8

This assignment allows GenAI tools with attribution. This log is that
attribution.

**Tool:** Claude (Anthropic), through Claude Code, November 2, 2026.

## How we worked

Claude wrote the code, the README and first drafts of the explanations,
recommended the design choices, and ran every check. I reviewed every file
with it, section by section and line by line, asking questions until I could
explain each part, and made the final calls. The video is me explaining the
finished code.

The review covered constructors and `self`, inheritance and overriding,
imports, testing, data cleaning, sample vs. population, covariance vs.
correlation, and Simpson's paradox.

## What came from me

- The Question 4 takeaways, in my own words.
- The raise convention: `applyRaise(10)` is a 10% raise.
- Reviewing and keeping Claude's other recommendations: the dataset, how the
  subclasses call their parents' constructors, the robot's salary, the tests,
  and the two columns for the correlation.

## How the work was checked

- Every script runs cleanly, and all of the Question 3 tests pass.
- Deliberately broken copies of the code were caught by the tests.
- pylint scores 10.00/10.
- Claude rendered and reviewed the charts, and fixed errors it found in its own
  explanations along the way.

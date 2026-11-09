# Assignment 9: Preprocessing and Data Visualization

Question 1 preprocesses the UCI Automobile dataset (205 imported cars from 1985), covering every
preprocessing step from the Lecture 9 list. Question 2 tells the data's story in five charts,
each colored by where the car's brand comes from. Question 3 runs a one-way ANOVA on price per
horsepower across those origins.

## Files

| File | What it holds |
|---|---|
| `homework_9_answers.ipynb` | All three questions: code, output, charts and explanations |
| `imports-85.data` | The data, exactly as downloaded from UCI (no header row) |
| `imports-85.names` | UCI's documentation: column names, documented ranges, missing-value counts |
| `automobile_clean.csv` | Question 1's output, used by Questions 2 and 3: 201 cars, 34 columns |
| `q2_1_cars_per_make.png` | Chart 1: one square per car, by make, grouped by origin |
| `q2_2_price_by_make.png` | Chart 2: every car's price by make, sorted by median price |
| `q2_3_engine_vs_fuel_use.png` | Chart 3: engine size vs. city fuel use, with each origin's average |
| `q2_4_horsepower_by_cylinders.png` | Chart 4: horsepower by cylinders, standard vs. turbo |
| `q2_5_fuel_type_mileage.png` | Chart 5: gas vs. diesel city mpg by origin |
| `q3_price_per_horsepower.png` | Question 3's chart: price per horsepower by origin |
| `AI_COLLABORATION.md` | How GenAI was used, and who did what |

## How to run

Python 3.11 or newer, with pandas, numpy, scipy and matplotlib, which are all in the repo's
`requirements.txt`. Welch's ANOVA needs scipy 1.16 or newer. Tested with Python 3.14.6,
pandas 3.0.3, numpy 2.4.6, scipy 1.18.0 and matplotlib 3.11.0.

Keep the data files in the same folder as the notebook, then run every cell from the top
(Restart Kernel and Run All). From a terminal:

```
jupyter nbconvert --to notebook --execute homework_9_answers.ipynb
```

Linting, with the repo's settings (scores 10.00/10):

```
python -m nbqa pylint homework_9_answers.ipynb --rcfile=../../.pylintrc
```

## Results in brief

- **Question 1:** 205 cars become 201, because the 4 cars with no price are dropped. No value is
  outside its documented range. The 28 statistical extremes are all real cars, so they are kept.
- **Question 2:** Japanese brands supply 53% of the cars, and the seven most expensive makes by
  median price are all European.
- **Question 3:** the null hypothesis is rejected (one-way ANOVA F(2, 196) = 77.9, p < 1e-15,
  confirmed by Welch's ANOVA and Kruskal-Wallis). European cars charged about $50 to $65 more
  per horsepower than Japanese and American brands.

## Data source

Jeffrey Schlimmer, Automobile dataset (1985), UCI Machine Learning Repository:
https://archive.ics.uci.edu/dataset/10/automobile. According to its documentation, the data
comes from the 1985 Model Import Car and Truck Specifications and the 1985 Ward's Automotive
Yearbook.

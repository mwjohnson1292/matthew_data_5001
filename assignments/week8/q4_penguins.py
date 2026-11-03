"""Question 4: basic data analysis of the Palmer Penguins dataset.

Data: 344 penguins of three species (Adelie, Chinstrap, Gentoo) on three
islands near Palmer Station, Antarctica, 2007 to 2009. Collected by
Dr. Kristen Gorman with the Palmer Station LTER program; packaged as
palmerpenguins by Allison Horst, Alison Hill and Kristen Gorman
(doi:10.5281/zenodo.3960218). License: CC-0.
Site: https://allisonhorst.github.io/palmerpenguins
File: penguins.csv, saved beside this script from
https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv

Steps: 1. load and describe; 2. summary statistics; 3. covariance and
correlation of bill length and depth; 4. the chart and takeaways.

Run it with:  python q4_penguins.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---- settings ----

# Paths relative to this script's folder, so it runs from any folder.
HERE = Path(__file__).parent
DATA_FILE = HERE / "penguins.csv"
BILLS_CHART = HERE / "q4_bill_length_vs_depth.png"

# The measurements analyzed. "year" is a label, not a measurement.
MEASUREMENTS = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

# Axis labels, with units.
LABELS = {
    "bill_length_mm": "Bill length (mm)",
    "bill_depth_mm": "Bill depth (mm)",
    "flipper_length_mm": "Flipper length (mm)",
    "body_mass_g": "Body mass (g)",
}

# The pair for step 3.
X_COL = "bill_length_mm"
Y_COL = "bill_depth_mm"

# One color per species, used in both charts.
SPECIES_COLORS = {"Adelie": "darkorange", "Chinstrap": "purple", "Gentoo": "teal"}


# ---- helpers ----

def section(title):
    """Print a section heading."""
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def two_decimals(value):
    """Format a number like 1,234.57."""
    return f"{value:,.2f}"


def correlation(x, y):
    """Return the Pearson correlation: [0, 1] of np.corrcoef's 2x2 grid."""
    return np.corrcoef(x, y)[0, 1]


def add_trend_line(ax, x, y, color):
    """Draw the least-squares straight line (np.polyfit, degree 1)."""
    slope, intercept = np.polyfit(x, y, 1)
    ends = np.array([x.min(), x.max()])
    ax.plot(ends, slope * ends + intercept, color=color, linewidth=2)


# ---- step 1: load and describe ----

def load_penguins():
    """Read penguins.csv. The text "NA" becomes a missing value."""
    return pd.read_csv(DATA_FILE)


def describe_dataset(penguins):
    """Step 1: print the shape, types, missing values and counts."""
    section("1. THE DATASET")
    rows, columns = penguins.shape  # a (rows, columns) tuple
    print(f"{rows} penguins (rows), {columns} columns: one row per penguin.")
    print("Each penguin has a species, an island, four measurements, a sex and a year.\n")

    print("Missing values per column:")
    print(penguins.isna().sum().to_string())

    print("\nPenguins per species and island:")
    print(pd.crosstab(penguins["species"], penguins["island"]))

    print("\nFirst five rows:")
    print(penguins.head())


def drop_unmeasured(penguins):
    """Drop penguins with no measurements; keep those missing only sex (unused)."""
    measured = penguins.dropna(subset=MEASUREMENTS)
    dropped = len(penguins) - len(measured)
    print(f"\nKept {len(measured)} of {len(penguins)} penguins; "
          f"{dropped} had no measurements and were dropped.")
    return measured


# ---- step 2: summary statistics ----

def summary_table(measured):
    """Step 2: mean, median, mode, std and variance, one row per statistic."""
    data = measured[MEASUREMENTS]

    modes = data.mode()  # one row back means no column has a tie
    assert len(modes) == 1, "a column has tied modes; report all of them"

    table = pd.DataFrame({
        "mean": data.mean(),
        "median": data.median(),
        "mode": modes.iloc[0],
        # pandas' .std() and .var() default to the sample versions (n - 1).
        "std (sample)": data.std(),
        "variance (sample)": data.var(),
    })
    return table.T  # flip so each statistic is a row


def show_summary(measured):
    """Step 2: print the summary table and the sample-vs-population choice."""
    section("2. SUMMARY STATISTICS (342 measured penguins)")
    table = summary_table(measured)
    # Pass the function itself (no parentheses); pandas calls it on each number.
    with pd.option_context("display.float_format", two_decimals):
        print(table)

    print("\nSample or population? It depends on the question.")
    print("The question is about the three species, and these 342 penguins stand")
    print("in for all of them. That makes them a sample: divide by n - 1 (ddof=1).")
    print("If the question were only about these 342 birds, they would be the")
    print("population, and dividing by n (ddof=0) would be right.")


# ---- step 3: covariance and correlation ----

def show_covariance_and_correlation(measured):
    """Step 3: covariance and correlation of bill length and depth."""
    section("3. COVARIANCE AND CORRELATION: BILL LENGTH vs. BILL DEPTH")

    print("Correlation of every pair of measurements:")
    print(measured[MEASUREMENTS].corr().round(2))

    print("\nWhy these two: bigger penguins are bigger everywhere, so most pairs")
    print("are positive. Bill depth is negative with everything, and bill length")
    print("and depth measure the same bill. That made no sense, so that's the pair.")

    x = measured[X_COL]
    y = measured[Y_COL]
    cov_xy = np.cov(x, y)[0, 1]  # [0, 1] of np.cov's 2x2 grid; divides by n - 1
    # Correlation is covariance divided by both standard deviations: no units, -1 to 1.
    r_all = correlation(x, y)

    print(f"\nAll penguins: covariance = {cov_xy:.2f} mm^2")
    print(f"All penguins: correlation = {r_all:.3f}")
    print("Negative and weak: longer bills come with slightly shallower bills.")

    # The same numbers within each species.
    rows = []
    for species, group in measured.groupby("species"):
        rows.append({
            "species": species,
            "penguins": len(group),
            "covariance": np.cov(group[X_COL], group[Y_COL])[0, 1],
            "correlation": correlation(group[X_COL], group[Y_COL]),
        })
    by_species = pd.DataFrame(rows).set_index("species")
    print("\nWithin each species:")
    print(by_species.round(3))
    print("\nPositive in every species. Gentoo bills are long and shallow, Adelie")
    print("bills short and deep, so pooling them flips the sign (Simpson's paradox).")
    print("Covariance carries units, so compare the correlations.")
    return r_all, by_species


# ---- step 4: chart and takeaways ----

def plot_bill_relationship(measured, r_all, by_species):
    """Chart 2: bill length vs. depth, all penguins (left) and by species (right)."""
    fig, (ax_all, ax_species) = plt.subplots(1, 2, figsize=(12, 5.2),
                                             sharex=True, sharey=True)

    ax_all.scatter(measured[X_COL], measured[Y_COL], color="gray", alpha=0.6, s=16)
    add_trend_line(ax_all, measured[X_COL], measured[Y_COL], "black")
    ax_all.set_title(f"All penguins together: r = {r_all:.2f}")

    for species, color in SPECIES_COLORS.items():
        group = measured[measured["species"] == species]
        r_species = by_species.loc[species, "correlation"]
        ax_species.scatter(group[X_COL], group[Y_COL], color=color, alpha=0.6, s=16,
                           label=f"{species}: r = {r_species:.2f}")
        add_trend_line(ax_species, group[X_COL], group[Y_COL], color)
    ax_species.set_title("Split by species: every trend is positive")
    ax_species.set_ylim(top=23.3)  # room for the legend above the data
    ax_species.legend(loc="upper center", ncol=3, fontsize=9, frameon=False)

    for ax in (ax_all, ax_species):
        ax.set_xlabel(LABELS[X_COL])
    ax_all.set_ylabel(LABELS[Y_COL])
    fig.suptitle("Bill length vs. bill depth: the species hide the real relationship",
                 fontsize=14)
    fig.tight_layout()
    fig.savefig(BILLS_CHART, dpi=150)
    plt.close(fig)


def show_takeaways(measured, r_all, by_species):
    """Step 4: my takeaways, with the numbers behind them."""
    section("4. TAKEAWAYS")
    low_r = by_species["correlation"].min()
    high_r = by_species["correlation"].max()
    species_means = measured.groupby("species")[MEASUREMENTS].mean()

    print("1. The side-by-side bill chart is a great example of dual encoding:")
    print("   the scatter, the trend lines and the color, side by side. Looking at")
    print(f"   the whole population of penguins is misleading (r = {r_all:.2f}).")
    print("   Colored by species, the scatter begins to tell the whole story on")
    print("   its own, and the trend lines become self-evident")
    print(f"   (r = {low_r:.2f} to {high_r:.2f} inside each species).")
    print("2. Chinstrap matches up with Gentoo on bill length, but otherwise")
    print("   Chinstrap and Adelie match up on bill depth, flipper length and")
    print("   body mass. Averages per species:")
    print(species_means.round(1).to_string())
    print("3. Look at specific species of penguins. It's hard to compare across")
    print("   penguin species.")
    print("4. The same whole-vs-part effect would likely show up at work: field")
    print("   operations broken out by region could tell a different story than")
    print("   the number for the whole country.")
    print(f"\nChart saved: {BILLS_CHART.name}")


def main():
    """Run the four steps in order."""
    pd.set_option("display.width", 120)
    pd.set_option("display.max_columns", 20)

    penguins = load_penguins()
    describe_dataset(penguins)
    measured = drop_unmeasured(penguins)
    show_summary(measured)
    r_all, by_species = show_covariance_and_correlation(measured)
    plot_bill_relationship(measured, r_all, by_species)
    show_takeaways(measured, r_all, by_species)


if __name__ == "__main__":
    main()

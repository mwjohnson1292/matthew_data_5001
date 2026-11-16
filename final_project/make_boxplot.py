"""Draw the proposal's chart: orbital distance by discovery method.

Reads the saved snapshot, keeps the four main discovery methods, and draws
one box per method on a log scale, with the habitable zone of a Sun-like
star shaded for reference. Also prints the count, median and quartiles
behind each box.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
SNAPSHOT = HERE / "data" / "pscomppars_2026-11-16.csv"
FIGURE = HERE / "figures" / "orbital_distance_by_method.png"
METHODS = ["Transit", "Radial Velocity", "Microlensing", "Imaging"]

# The habitable zone of our own Sun, from Kopparapu et al. (2013). The zone
# sits closer in for dimmer stars and farther out for brighter ones.
SUN_ZONE_AU = (0.99, 1.70)

# One color for every box: the method is already named on the axis.
BLUE = "#2a78d6"
ZONE_COLOR = "#1baf7a"
INK = "#0b0b0b"
GRAY = "#52514e"
SURFACE = "#fcfcfb"


def load_planets(path: Path) -> pd.DataFrame:
    """Load the snapshot and keep the planets the proposal analyzes.

    Args:
        path: The snapshot CSV saved by pull_data.py.

    Returns:
        Planets found by one of the four main methods that have a recorded
        orbital distance, with a log10 distance column added.
    """
    planets = pd.read_csv(path)
    keep = planets["discoverymethod"].isin(METHODS) & planets["pl_orbsmax"].notna()
    planets = planets[keep].copy()
    planets["log_distance"] = np.log10(planets["pl_orbsmax"])
    return planets


def summarize(planets: pd.DataFrame) -> pd.DataFrame:
    """Describe orbital distance (AU) for each method, closest first.

    Args:
        planets: The filtered planets from load_planets.

    Returns:
        One row per method with count, quartiles, minimum and maximum,
        sorted by median distance.
    """
    summary = planets.groupby("discoverymethod")["pl_orbsmax"].describe()
    summary = summary[["count", "min", "25%", "50%", "75%", "max"]]
    return summary.sort_values("50%")


def draw_boxplot(planets: pd.DataFrame, order: list[str]) -> None:
    """Draw and save the box plot.

    The boxes are computed on log10 distance, so the whiskers and outliers
    follow the log scale the chart is read on. Computed on raw AU, the
    whiskers would be squashed against the box and thousands of points
    would count as outliers.

    Args:
        planets: The filtered planets from load_planets.
        order: Method names in the order to draw them, left to right.
    """
    groups = [planets.loc[planets["discoverymethod"] == m, "log_distance"] for m in order]
    labels = [f"{m}\n(n = {len(g):,})" for m, g in zip(order, groups)]

    fig, ax = plt.subplots(figsize=(8, 5.5), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.boxplot(
        groups,
        widths=0.5,
        patch_artist=True,
        boxprops={"facecolor": BLUE, "alpha": 0.35, "edgecolor": BLUE},
        medianprops={"color": INK, "linewidth": 2},
        whiskerprops={"color": BLUE},
        capprops={"color": BLUE},
        flierprops={"marker": "o", "markersize": 3, "markerfacecolor": BLUE,
                    "markeredgecolor": "none", "alpha": 0.25},
    )
    ax.set_xticks(range(1, len(order) + 1), labels)

    # The data is log10(AU); label the axis in plain AU.
    powers = range(-3, 5)
    ax.set_yticks(list(powers), [f"{10.0 ** p:,g}" for p in powers])
    ax.set_ylabel("Orbital distance from star (AU, log scale)", color=GRAY)

    # Shade the Sun's habitable zone, drawn behind the boxes.
    low, high = np.log10(SUN_ZONE_AU)
    ax.axhspan(low, high, color=ZONE_COLOR, alpha=0.25, linewidth=0, zorder=0)
    ax.text(len(order) + 0.45, low - 0.12,
            f"Habitable zone of a\nSun-like star ({SUN_ZONE_AU[0]}–{SUN_ZONE_AU[1]:.2f} AU)",
            color=GRAY, ha="right", va="top", fontsize=9)

    ax.set_title("Orbital distance of confirmed exoplanets, by discovery method",
                 color=INK, loc="left")
    ax.grid(axis="y", color=GRAY, alpha=0.15)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=GRAY)
    fig.text(0.01, 0.01, "Source: NASA Exoplanet Archive, snapshot of 2026-11-16",
             color=GRAY, fontsize=8)

    FIGURE.parent.mkdir(exist_ok=True)
    fig.savefig(FIGURE, dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    kept = load_planets(SNAPSHOT)
    table = summarize(kept)
    print(table.round(3).to_string())
    draw_boxplot(kept, list(table.index))
    print(f"Saved {FIGURE.name}")

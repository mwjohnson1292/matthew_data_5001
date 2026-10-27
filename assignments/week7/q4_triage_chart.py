"""Assignment 7, Question 4: tell the data's story with another library.

Question: What other analysis would make sense here? Find another library or tool
that you think would help tell this data's story. Demonstrate using it in some way.

Answer: A triage ranking. A beekeeper has limited time, so the most useful
analysis ranks the hives from most to least in need of attention, and shows why,
so they can act first where it is needed most. hive/triage.py ranks each hive by
the risk score at its latest inspection, because triage is about the hive's state
now, and breaks ties by mite count, the largest single risk factor.

The library is matplotlib, the most widely used Python library for static
charts. It draws the ranking as a horizontal bar chart, saved as
q4_triage_chart.png: the most urgent hive at the top, bar length showing the
degree of urgency, and each hive's risk reasons beside its bar. Color follows the
risk band (green low, amber review, red urgent), and every bar also carries the
band's name, so the chart never relies on color alone; red and green are hard to
tell apart for many colorblind readers.

What the chart shows: three hives need attention, and all three scored worse than
at their previous inspection. H-06 is the only one that was already flagged and
is still climbing (6 to 8). The other three have no risk factors, so the
beekeeper's time goes, in order, to H-06, H-03 and H-01.

With more data: these are 11 inspections over about three weeks, with three
measurable weight changes, so statistics on them would be guesses. With a full
season, the next analyses would be each hive's risk and weight trend over time,
and whether rising mite counts come before weight loss.

Run with:
    python q4_triage_chart.py
This file must stay next to the hive/ folder: Python looks for hive in the
folder that holds the script, not the folder you run it from.
"""
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt

from hive.pipeline import run_pipeline
from hive.risk import MITE_POINTS, QUEEN_MISSING_POINTS, TEMP_POINTS, WEIGHT_LOSS_POINTS
from hive.summary import REVIEW_MIN_SCORE, URGENT_MIN_SCORE
from hive.triage import rank_hives

# The chart is saved next to this script, wherever it is run from
CHART_PATH = Path(__file__).with_name("q4_triage_chart.png")

# Highest possible score: every risk condition at once
MAX_SCORE = MITE_POINTS + QUEEN_MISSING_POINTS + WEIGHT_LOSS_POINTS + TEMP_POINTS

# Status colors mean good -> bad, so they are reserved for the risk bands
BAND_COLORS = {"low": "#0ca30c", "review": "#fab219", "urgent": "#d03b3b"}

# Text and chart chrome stay neutral so color only ever means risk
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
SURFACE = "#fcfcfb"


# ---- Tests ----

def make_record(hive_id, day, risk_score, mites):
    """A minimal scored record with only the fields rank_hives reads."""
    return {"hive_id": hive_id, "inspection_date": date(2026, 9, day),
            "risk_score": risk_score, "mites": mites, "risk_reasons": []}


def test_rank_hives():
    """Latest score decides the rank, mites break ties, one inspection has no previous."""
    ranked = rank_hives([
        make_record("H-10", 1, 8, 14),   # was urgent, but its latest score is 0
        make_record("H-10", 15, 0, 2),
        make_record("H-11", 1, 3, 4),    # ties H-12 on score, has fewer mites
        make_record("H-12", 1, 3, 9),
    ])
    assert [hive["hive_id"] for hive in ranked] == ["H-12", "H-11", "H-10"]
    assert ranked[2]["previous_score"] == 8 and ranked[2]["risk_label"] == "low"
    assert ranked[0]["previous_score"] is None
    print("All triage ranking tests passed")


# ---- The chart ----

def trend_text(hive):
    """How the score moved since the hive's previous inspection."""
    if hive["previous_score"] is None:
        return "only one usable inspection"
    if hive["risk_score"] > hive["previous_score"]:
        return f"▲ up from {hive['previous_score']}"
    if hive["risk_score"] < hive["previous_score"]:
        return f"▼ down from {hive['previous_score']}"
    return "no change"


def reasons_text(hive):
    """The risk reasons, or the mite count when there are none."""
    if hive["risk_reasons"]:
        return "  ·  ".join(hive["risk_reasons"])
    return f"no risk factors  ·  {hive['mites']} mites"


def headline(ranked):
    """Title that states the takeaway, built from the data so it stays true."""
    top = ranked[0]
    title = f"Visit {top['hive_id']} first: {top['risk_label']}"
    if top["previous_score"] is not None and top["risk_score"] > top["previous_score"]:
        title += ", and worse than its last inspection"
    return title


def draw_triage_chart(ranked, path):
    """Draw the ranked hives as horizontal bars and save the chart as a PNG."""
    fig, ax = plt.subplots(figsize=(11, 4.8), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.07, right=0.46, top=0.80, bottom=0.14)

    rows = range(len(ranked))
    ax.barh(rows, [hive["risk_score"] for hive in ranked], height=0.5,
            color=[BAND_COLORS[hive["risk_label"]] for hive in ranked])

    for row, hive in zip(rows, ranked):
        # The score at the end of each bar
        ax.text(hive["risk_score"] + 0.12, row, str(hive["risk_score"]),
                va="center", fontsize=10, fontweight="bold", color=INK)
        # Right of the plot: the band name and trend, then the reasons.
        # x is a fraction of the plot's width (1.0 is its right edge), y is the row
        ax.text(1.04, row - 0.13, f"{hive['risk_label'].upper()}   {trend_text(hive)}",
                transform=ax.get_yaxis_transform(), va="center",
                fontsize=9.5, fontweight="bold", color=INK)
        ax.text(1.04, row + 0.2, reasons_text(hive),
                transform=ax.get_yaxis_transform(), va="center",
                fontsize=8.5, color=INK_SECONDARY)

    # Where the review and urgent bands begin
    for threshold, name in [(REVIEW_MIN_SCORE, "review"), (URGENT_MIN_SCORE, "urgent")]:
        ax.axvline(threshold, color=INK_MUTED, linestyle="--", linewidth=0.8)
        # Label sits just right of its line, so the line never crosses the text
        ax.text(threshold + 0.08, -0.62, f"{name} from {threshold}", ha="left", va="bottom",
                fontsize=8, color=INK_MUTED)

    # Most urgent at the top: row 0 is drawn first, so flip the y axis
    ax.set_ylim(len(ranked) - 0.5, -0.75)
    ax.set_yticks(list(rows), [hive["hive_id"] for hive in ranked],
                  fontsize=10, fontweight="bold", color=INK)
    # Extra room past the maximum so the top score's label clears the text column;
    # the axis line itself still stops at the maximum
    ax.set_xlim(0, MAX_SCORE + 0.8)
    ax.set_xticks(range(MAX_SCORE + 1))
    ax.spines["bottom"].set_bounds(0, MAX_SCORE)
    ax.set_xlabel(f"Risk score at latest inspection (points, 0 to {MAX_SCORE})",
                  fontsize=9, color=INK_SECONDARY)
    ax.tick_params(axis="x", colors=INK_MUTED, labelsize=9)
    ax.tick_params(axis="y", length=0)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(INK_MUTED)

    first = min(hive["latest_date"] for hive in ranked)
    last = max(hive["latest_date"] for hive in ranked)
    fig.text(0.07, 0.93, headline(ranked), fontsize=14, fontweight="bold", color=INK)
    fig.text(0.07, 0.875,
             f"{len(ranked)} hives ranked by risk score at their latest inspection "
             f"({first:%b %d} to {last:%b %d, %Y}). Ties go to the hive with more mites.",
             fontsize=9.5, color=INK_SECONDARY)

    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def main():
    """Test the ranking, rank the real hives, print the order, and save the chart."""
    test_rank_hives()
    ranked = rank_hives(run_pipeline().scored)
    for hive in ranked:
        print(f"{hive['hive_id']}  score {hive['risk_score']}  {hive['risk_label']:<7}"
              f"{trend_text(hive)}")
    draw_triage_chart(ranked, CHART_PATH)
    print(f"Chart saved to {CHART_PATH.name}")


# Runs only when this file is executed directly, not when another file imports it
if __name__ == "__main__":
    main()

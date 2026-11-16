"""Download a dated snapshot of NASA's confirmed-exoplanet table.

Pulls the Planetary Systems Composite Parameters table (one row per confirmed
planet) from the NASA Exoplanet Archive's public API and saves it as a CSV
named for today's date. The archive adds planets every week, so the analysis
reads a saved snapshot instead of the live table and can be rerun on the
same data.
"""

from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd

API_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
TABLE = "pscomppars"
DATA_DIR = Path(__file__).parent / "data"

# Only the columns the four stages of the project use. The *_reflink columns
# hold the source of each value, including whether it was calculated.
COLUMNS = [
    "pl_name",
    "hostname",
    "discoverymethod",
    "disc_year",
    "pl_orbsmax",
    "pl_orbsmax_reflink",
    "pl_rade",
    "pl_rade_reflink",
    "pl_bmasse",
    "pl_bmasse_reflink",
    "pl_insol",
    "st_teff",
    "st_lum",
    "st_mass",
    "sy_dist",
]


def build_url() -> str:
    """Build the API request for the chosen columns, as CSV.

    Returns:
        The full request URL, with the query safely encoded.
    """
    query = f"select {','.join(COLUMNS)} from {TABLE}"
    return f"{API_URL}?{urlencode({'query': query, 'format': 'csv'})}"


def download_snapshot() -> Path:
    """Download the table and save it unchanged under today's date.

    Returns:
        The path of the saved CSV file.

    Raises:
        ValueError: If the response is not the table (for example, an error
            page), so a bad download is never saved as data.
    """
    with urlopen(build_url(), timeout=120) as response:
        raw = response.read()

    # The first column requested is pl_name, so a real answer starts with it.
    if not raw.startswith(b"pl_name"):
        raise ValueError(f"unexpected response, starts with {raw[:60]!r}")

    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / f"{TABLE}_{date.today().isoformat()}.csv"
    path.write_bytes(raw)
    return path


if __name__ == "__main__":
    saved = download_snapshot()
    planets = pd.read_csv(saved)
    print(f"Saved {len(planets):,} planets to {saved.name}")

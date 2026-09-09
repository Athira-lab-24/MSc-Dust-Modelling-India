# Author: Athira P T
# MSc Dissertation: Dust Modelling over the Indian Region
# Description: Compare boundary-layer depth with and without UKCA
# Period: 06–08 November 2017
# Time zone: IST

import glob
import os
from datetime import datetime, timedelta

import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


# ============================================================
# Configuration
# ============================================================

# Directory containing the model CSV files
DATA_DIR = "../data/boundary_layer_depth"

# File patterns
WITHOUT_UKCA_PATTERN = (
    "BOUNDARY_LAYER_DEPTH_AFTER_TIMESTEP_201711*_surface.csv"
)

WITH_UKCA_PATTERN = (
    "BOUNDARY_LAYER_DEPTH_AFTER_TIMESTEP_201711*_surface_UKCA.csv"
)

# Variable to plot
PBL_VARIABLE = "BOUNDARY_LAYER_DEPTH_AFTER_TIMESTEP"


# ============================================================
# Function to process model files
# ============================================================

def process_files(file_pattern):
    """
    Read boundary-layer-depth CSV files, convert forecast period
    to IST, and calculate the spatial mean for each time.
    """

    dataframes = []

    search_pattern = os.path.join(DATA_DIR, file_pattern)

    for filename in sorted(glob.glob(search_pattern)):

        print(f"Reading file: {filename}")

        # Extract initialization date from filename
        date_str = os.path.basename(filename).split("_")[5]

        init_time = datetime.strptime(date_str, "%Y%m%d")

        # Read CSV
        df = pd.read_csv(filename)

        # Convert forecast period to UTC
        df["datetime_utc"] = df["forecast_period"].apply(
            lambda hours: init_time + timedelta(hours=hours)
        )

        # Convert UTC to IST
        df["datetime_ist"] = df["datetime_utc"] + timedelta(
            hours=5, minutes=30
        )

        dataframes.append(df)

    # Check whether files were found
    if not dataframes:
        raise FileNotFoundError(
            f"No files found for pattern: {search_pattern}"
        )

    # Combine all daily files
    all_data = pd.concat(dataframes, ignore_index=True)

    # Calculate spatial mean for each time
    grouped_data = (
        all_data
        .groupby("datetime_ist")[PBL_VARIABLE]
        .mean()
        .reset_index()
    )

    # Sort chronologically
    grouped_data.sort_values("datetime_ist", inplace=True)

    return grouped_data


# ============================================================
# Process the two model experiments
# ============================================================

df_without_ukca = process_files(WITHOUT_UKCA_PATTERN)

df_with_ukca = process_files(WITH_UKCA_PATTERN)


# ============================================================
# Plot boundary-layer depth
# ============================================================

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    df_without_ukca["datetime_ist"],
    df_without_ukca[PBL_VARIABLE],
    marker="o",
    label="Without UKCA"
)

ax.plot(
    df_with_ukca["datetime_ist"],
    df_with_ukca[PBL_VARIABLE],
    marker="s",
    label="With UKCA"
)


# ============================================================
# Format axes
# ============================================================

ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%d-%b %H:%M")
)

ax.xaxis.set_major_locator(
    mdates.HourLocator(interval=6)
)

ax.set_xlabel("Time (IST)")
ax.set_ylabel("Boundary Layer Depth (m)")
ax.set_title("Boundary Layer Depth: With and Without UKCA")

plt.xticks(rotation=45)

ax.legend()

plt.tight_layout()


# ============================================================
# Save figure
# ============================================================

output_file = "boundary_layer_depth_comparison_IST.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

print(f"Figure saved as: {output_file}")

plt.show()

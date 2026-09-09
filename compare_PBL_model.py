import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import glob

# File patterns
file_pattern = "BOUNDARY_LAYER_DEPTH_AFTER_TIMESTEP_201711*_surface.csv"
file_pattern01 = "BOUNDARY_LAYER_DEPTH_AFTER_TIMESTEP_201711*_surface_UKCA.csv"

# Function to process a set of files
def process_files(pattern):
    all_data = pd.DataFrame()
    for filename in sorted(glob.glob(pattern)):
        print("Reading file:", filename)
        date_str = filename.split('_')[5]
        init_time = datetime.strptime(date_str, "%Y%m%d")
        df = pd.read_csv(filename)
        df['datetime_utc'] = df['forecast_period'].apply(lambda x: init_time + timedelta(hours=x))
        df['datetime_ist'] = df['datetime_utc'].apply(lambda dt: dt + timedelta(hours=5, minutes=30))
        all_data = all_data.append(df, ignore_index=True)
    df_grouped = all_data.groupby('datetime_ist')['BOUNDARY_LAYER_DEPTH_AFTER_TIMESTEP'].mean().reset_index()
    df_grouped.sort_values('datetime_ist', inplace=True)
    return df_grouped

# Process both sets
df_obs = process_files(file_pattern)
df_ukca = process_files(file_pattern01)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(df_obs['datetime_ist'], df_obs['BOUNDARY_LAYER_DEPTH_AFTER_TIMESTEP'], marker='o', color='#a65628', label='Without UKCA')
plt.plot(df_ukca['datetime_ist'], df_ukca['BOUNDARY_LAYER_DEPTH_AFTER_TIMESTEP'], marker='s', color='#4daf4a', label='With UKCA')

# Format x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))

# Labels and legend
plt.title("Boundary Layer Depth")
plt.xlabel("Time (IST)")
plt.ylabel("Height (m)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Save and show plot
plt.savefig("pbl_comparison_IST_3days.png")
plt.show()

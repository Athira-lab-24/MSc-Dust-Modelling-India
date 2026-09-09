# Author: Athira P T
# MSc Dissertation: Dust Modelling over the Indian Region
# Description: Plot model-aeronet VSD 


import pandas as pd
import matplotlib.pyplot as plt

# File paths
model_file_path1 =[ "../data/mean_volume_size_distribution_kanpur_insol_dm_042017.csv"
                   "../data/mean_volume_size_distribution_kanpur082018.csv"
                   "../data/mean_volume_size_distribution_kanpur092018.csv"
]
#aeronet_file_path = "PATH_TO_AERONET_VSD_FILE"

# Read the first model file
model_df1 = pd.read_csv(model_file_path1)
model_df1["Radius"] = model_df1["Diameter"] / 2  # Convert diameter to radius
model_radii1 = model_df1["Radius"]
dv_dlnd_model1 = model_df1["Mean Volume Size Distribution"]

# Read the second model file
#model_df2 = pd.read_csv(model_file_path2)
#model_df2["Radius"] = model_df2["Diameter"] / 2  # Convert diameter to radius
#model_radii2 = model_df2["Radius"]
#dv_dlnd_model2 = model_df2["Mean Volume Size Distribution"]

# Read the second model file
#model_df3 = pd.read_csv(model_file_path3)
#model_df3["Radius"] = model_df3["Diameter"] / 2  # Convert diameter to radius
#model_radii3 = model_df3["Radius"]
#dv_dlnd_model3 = model_df3["Mean Volume Size Distribution"]

# Read AERONET file
#aeronet_df = pd.read_csv(aeronet_file_path, skiprows=6, header=None)

# Extract radius values
#radius = aeronet_df.iloc[0, 5:27].values.astype(float)

# Select specific rows for AERONET volume size distribution
#dv_dlnr_aeronet1 = aeronet_df.iloc[33, 5:27].values.astype(float)
#dv_dlnr_aeronet2 = aeronet_df.iloc[35, 5:27].values.astype(float)
#dv_dlnr_aeronet3 = aeronet_df.iloc[40, 5:27].values.astype(float)

# Create a plot with two y-axes
fig, ax1 = plt.subplots(figsize=(8, 6))

# Left y-axis (AERONET data: dv/dlnr)
#ax1.plot(radius, dv_dlnr_aeronet1, 'c--', label="AERONET dv/dlnr[07/05/2018]")
#ax1.plot(radius, dv_dlnr_aeronet3, 'go-', label="AERONET dv/dlnr[08/05/2018]")
#ax1.plot(radius, dv_dlnr_aeronet3, 'ro-', label="AERONET dv/dlnr[09/05/2018]")
#ax1.set_xlabel("Radius ($\mu$m)")
#ax1.set_ylabel(r"dv/dlnr (AERONET) ($\mu m^3 / \mu m^2$)", color="blue")
#ax1.tick_params(axis='y', labelcolor="blue")
ax1.set_xscale("log")
#ax1.set_ylim(0,1)
ax1.set_yscale("log")
# Right y-axis (Model data: dv/dlnd)
ax2 = ax1.twinx()
ax2.plot(model_radii1, dv_dlnd_model1, 'c-', label="Model dv/dlnd (04/11/2017)")
#ax2.plot(model_radii2, dv_dlnd_model2, 'm', label="Model dv/dlnd (08/05/2018)")
#ax2.plot(model_radii3, dv_dlnd_model3, 'y', label="Model dv/dlnd (09/05/2018)")
ax2.set_ylabel(r"dv/dlnd (Model) ($\mu m^3 / cm^3$)", color="red")
ax2.tick_params(axis='y', labelcolor="red")
#ax2.set_ylim(0,100)
ax2.set_yscale("log")

# Adjust legend placement
ax1.legend(loc='upper left', bbox_to_anchor=(0.01, 1.02))
ax2.legend(loc='upper right', bbox_to_anchor=(0.99, 1.02))

plt.title("Volume Size Distribution: AERONET  vs Model ")
#plt.savefig("volume_AERONET_vs_Model.png")
#plt.savefig("volume_AERONET_vs_Model_kanpur_2018.png")

plt.show()



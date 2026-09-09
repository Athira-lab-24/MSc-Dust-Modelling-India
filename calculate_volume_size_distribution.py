# Author: Athira P T
# MSc Dissertation: Dust Modelling over the Indian Region
# Description: calculate mean aerosol VSD from Model output

import pandas as pd
import numpy as np

# Load data
vol_acc_file = "../data/first_height_level_vol_conc_acc_insol_09.csv"
dia_acc_file = "../data/first_height_level_dry_dia_acc_insol_09.csv"
vol_coarse_file = "../data/first_height_level_vol_conc_coarse_insol_09.csv"
dia_coarse_file = "../data/first_height_level_dry_dia_coarse_insol_09.csv"

df_acc_vol = pd.read_csv(vol_acc_file)
df_acc_dia = pd.read_csv(dia_acc_file)
df_coarse_vol = pd.read_csv(vol_coarse_file)
df_coarse_dia = pd.read_csv(dia_coarse_file)

# Extract volume concentrations and convert to 
V_acc = df_acc_vol['VOL_CONC_ACC_INSOL'].values * 1e18  
D_bar_acc = df_acc_dia['DRY_DIA_ACC_INSOL'].values * 1e+06  

V_coarse = df_coarse_vol['VOL_CONC_COARSE_INSOL'].values * 1e18  
D_bar_coarse = df_coarse_dia['DRY_DIA_COARSE_INSOL'].values * 1e+06  

# Define geometric standard deviations
sigma_acc = 1.59  # Accumulation mode
sigma_coarse = 2.0  # Coarse mode

# Compute volume-median diameters
D_V_bar_acc = D_bar_acc * np.exp(3 * (np.log(sigma_acc) ** 2))
D_V_bar_coarse = D_bar_coarse * np.exp(3 * (np.log(sigma_coarse) ** 2))

# Concatenate volume concentrations and diameters
V_total = np.concatenate((V_acc, V_coarse))
D_V_bar_total = np.concatenate((D_V_bar_acc, D_V_bar_coarse))

# Define a fixed diameter range for plotting (10^-1 to 10^2 m)
D = np.logspace(-1, 2, 100)

# Compute total volume size distribution
n_V_D_total = np.zeros((len(D_V_bar_total), len(D)))

for i in range(len(D_V_bar_total)):
    sigma = sigma_acc if i < len(D_V_bar_acc) else sigma_coarse  # Use correct sigma
    n_V_D_total[i, :] = (V_total[i] / (np.sqrt(2 * np.pi) * np.log(sigma))) * np.exp(
        -((np.log(D) - np.log(D_V_bar_total[i])) ** 2) / (2 * (np.log(sigma) ** 2))
    )

# Compute the mean distribution
mean_n_V_D_total = np.mean(n_V_D_total, axis=0)

output_file = "mean_volume_size_distribution_kanpur_09_2017.csv"
df_output.to_csv(output_file, index=False)

print(f"File saved as {output_file}")




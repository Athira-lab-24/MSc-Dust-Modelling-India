# Author: Athira P T
# MSc Dissertation: Dust Modelling over the Indian Region
# Description: Extract surface flux (downward SW and LW) from the model 


import iris
import pandas as pd
import os
from datetime import datetime, timedelta

dates = ['20171106','20171107','20171108']  # Add more dates as needed

for date in dates:
    today = date
    region = 'region'

    if region == 'region':
        lon1, lon2 = 74, 80.3
        lat1, lat2 = 26,30

    tDay = datetime.strptime(today, "%Y%m%d")
    yDay = (tDay - timedelta(days=1)).strftime('%Y%m%d')

    inpath = "PATH_TO_MODEL_OUTPUT/{}/gldust-00".format(today)

    # Define region constraint
    gcon = iris.Constraint(
        coord_values=dict(latitude=lambda cell: lat1 <= cell <= lat2,
                          longitude=lambda cell: lon1 <= cell <= lon2))

    # Define time constraint (forecast period between 12 and 35 hours)
    tconstr = iris.Constraint(forecast_period=lambda cell: 12 <= cell <= 35)

    # STASH codes to extract
    stash_codes = [
        ('m01s02i201', 'Net_downward_lw_flux'),
        ('m01s01i202', 'Net_downward_sw_flux'),
    ]

    # UM output files
    infile = ['umnsaa_pf018', 'umnsaa_pf024', 'umnsaa_pf030', 'umnsaa_pf036']
    infiless1 = []

    # Filter only existing files
    for ifile in infile:
        full_path = os.path.join(inpath, ifile)
        if os.path.exists(full_path):
            infiless1.append(full_path)
        else:
            print("WARNING: File not found - {}".format(full_path))

    # If no valid files remain, skip this date
    if not infiless1:
        print("ERROR: No valid input files found for date {}".format(today))
        continue

    # Process each variable
    for stash, shortname in stash_codes:
        STASHcon_alt = iris.AttributeConstraint(STASH=stash)

        try:
            cube_list = iris.load(infiless1, STASHcon_alt)
        except Exception as e:
            print("ERROR loading data for STASH {}: {}".format(stash, e))
            continue

        if not cube_list:
            print("No data found for STASH {}".format(stash))
            continue

        cube1 = cube_list[0]
        print("Loaded cube for {}: {}".format(shortname, cube1.summary(shorten=True)))

        cube = cube1.extract(gcon & tconstr)

        if cube is None:
            print("No matching data after applying constraints for STASH {}".format(stash))
            continue

        # Remove unnecessary coords if present
        for coord in ('sigma', 'model_level_number', 'level_height'):
            if cube.coords(coord):
                cube.remove_coord(coord)

        forecast_periods = cube.coord('forecast_period').points
        latitudes = cube.coord('latitude').points
        longitudes = cube.coord('longitude').points

        data_values = cube.data  # shape: time x lat x lon

        # Flatten 3D data
        data_list = []
        for t_idx, f_period in enumerate(forecast_periods):
            for lat_idx, lat in enumerate(latitudes):
                for lon_idx, lon in enumerate(longitudes):
                    value = data_values[t_idx, lat_idx, lon_idx]
                    data_list.append([f_period, lat, lon, value])

        # Create DataFrame
        df_cube = pd.DataFrame(data_list, columns=['forecast_period', 'latitude', 'longitude', shortname])

        # Save CSV
        output_file = "{}_{}_surface_UKCA.csv".format(shortname, today)
        df_cube.to_csv(output_file, index=False)
        print("Saved surface flux data to {}".format(output_file))



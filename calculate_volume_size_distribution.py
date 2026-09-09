import iris
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

dates = ['20171108']  # List of dates

for date in dates:
    today = date
    region = 'Kanpur'

    if region == 'Kanpur':
        lon1, lon2 = 80.1, 80.3
        lat1, lat2 = 26.4, 26.6

    tDay = datetime.strptime(today, "%Y%m%d")
    yDay = (tDay - timedelta(days=1)).strftime('%Y%m%d')

    inpath = '/home/ksapsara/CSM_output/irrig/fcst/20171108/00-CTL'

    gcon = iris.Constraint(
        coord_values=dict(latitude=lambda cell: lat1 <= cell <= lat2,
                          longitude=lambda cell: lon1 <= cell <= lon2))

    tconstr = iris.Constraint(forecast_period=lambda cell: 12 <= cell <= 35)

    stash_codes = [
        ('m01s38i403', 'dry_dia_acc_insol'),
        ('m01s38i404', 'dry_dia_coarse_insol'),
        ('m01s38i425', 'vol_conc_acc_insol'),
        ('m01s38i426', 'vol_conc_coarse_insol')
    ]

    infile = ['umnsaa_pd030', 'umnsaa_pf030', 'umnsaa_pf030', 'umnsaa_pf030']
    infiless1 = list(map(lambda ifile: os.path.join(inpath, ifile), infile))

    for stash, filename in stash_codes:
        STASHcon_alt = iris.AttributeConstraint(STASH=stash)
        cube_list = iris.load(infiless1, STASHcon_alt)
        
        if not cube_list:
            print("No data found for STASH {}".format(stash))
            continue

        cube1 = cube_list[0]
        print cube1 [4]
        cube = cube1.extract(gcon & tconstr)
         

        if cube is None:
            print("No matching data after applying constraints for STASH {}".format(stash))
            continue

        # Remove unnecessary coordinates
        for coord in ('sigma', 'model_level_number'):
            if cube.coords(coord):
                cube.remove_coord(coord)

        # Get coordinate values
        forecast_periods = cube.coord('forecast_period').points
        heights = cube.coord('level_height').points
        latitudes = cube.coord('latitude').points
        longitudes = cube.coord('longitude').points

        # Extract the 4D data (forecast_period, height, lat, lon)
        data_values = cube.data  # Shape: (time, height, lat, lon)

        # Flatten the data into a 2D table
        data_list = [[f_period, height, lat, lon, data_values[t_idx, h_idx, lat_idx, lon_idx]]
                     for t_idx, f_period in enumerate(forecast_periods)
                     for h_idx, height in enumerate(heights)
                     for lat_idx, lat in enumerate(latitudes)
                     for lon_idx, lon in enumerate(longitudes)]

        # Create DataFrame
        df_cube = pd.DataFrame(data_list, columns=['forecast_period', 'height', 'latitude', 'longitude', filename.upper()])

        # Save to CSV
        output_file = "{}_09.csv".format(filename)
        df_cube.to_csv(output_file, index=False)
        print("Saved data to {}".format(output_file))

        # Save first height level separately
        first_height = df_cube["height"].min()
        df_first_level = df_cube[df_cube["height"] == first_height]
        first_height_output = "first_height_level_{}_09.csv".format(filename)
        df_first_level.to_csv(first_height_output, index=False)
        print("Saved first height level data to {}".format(first_height_output))


import xarray as xr
import matplotlib.pyplot as plt
import geopandas as gpd

ds=xr.open_dataset(r"C:\Users\athir\Pictures\New folder\OneDrive\Desktop\NCMRWF\RESULTS\AOD\dod_20171107_NOV_AOD.nc")
#print (ds)

AOD_CLASSIC = ds['atmosphere_optical_thickness_due_to_aerosol']
#print(AOD_CLASSIC.dims)
#print(AOD_CLASSIC.shape)
AOD = AOD_CLASSIC.isel(time=0)
AOD.plot(
    x='longitude',
    y='latitude',
    vmin = 0,
    vmax = 3,
    cmap='viridis',
    cbar_kwargs ={'label':'AOD'}
)
india = gpd.read_file(
    r"C:\Users\athir\Downloads\maps-master\maps-master\States\Admin2.shp"
)
india.boundary.plot(
    ax=plt.gca(),
    color='black',
    linewidth=0.3
)
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.title('AOD from model CLASSIC scheme')
plt.show()

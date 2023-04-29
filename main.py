import pandas as pd
import numpy as np
import os
import rasterio
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.svm import SVR

# path to SAR data
path = r'C:\Usersname\Documents\ALOS2_TC2'

alos = [os.path.join(path, item) for item in os.listdir(path) if ('HH' in item or 'HV' in item)
        and item.endswith('.img') and os.path.isfile(os.path.join(path, item))]

alos.sort(key=lambda x: datetime.strptime(os.path.basename(x).split('_')[3], '%d%b%Y'))

fig = plt.figure(figsize=(12, 8))

for f, file in enumerate(alos):
    with rasterio.open(file) as src:
        alos_img = src.read(1)
        no_data = -3.4028230607370965e+38

        # Extracting zonal stats for each circular polygon
        alos_stats_list = []
        #loop over the images in the stack
        for i in range(alos_img.shape[0]):
            #assign a value to no data to match the one in data
            no_data = -3.4028230607370965e+38
            #extract stats value
            alos_stats = rs.zonal_stats(L2A_oct_gpd['geometry'],
                                       alos_img[i],
                                       nodata=no_data,
                                       affine=src.transform,
                                       geojson_out=True,
                                       copy_properties=True,
                                       stats="count min mean max median")

            # convert data into a geodataframe
            alos_stats_fr = gpd.GeoDataFrame.from_features(alos_stats)

            # add the image index as a new column
            alos_stats_fr['image_index'] = i

            # append the dataframe to the list
            alos_stats_list.append(alos_stats_fr)

# concatenate the dataframes in the list into a single dataframe
alos_stats_fr = pd.concat(alos_stats_list, ignore_index=True)

print(alos_stats_fr)
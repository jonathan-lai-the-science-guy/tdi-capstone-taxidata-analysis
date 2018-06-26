import pandas as pd
import gc

for i in [2009]:
    for j in range(1,13):
        print(i,j)
        PATH = "../Raw_Data/yellow_tripdata_{:4d}-{:02d}.csv.gz".format(i,j)
        tmp = pd.read_csv(PATH,\
                          engine='c',\
                          error_bad_lines=False)

        tmp["hour"] = pd.to_datetime(tmp["Trip_Pickup_DateTime"],\
                                     format="%Y/%m/%d %H:%M:%S",\
                                     errors='ignore',\
                                     box=True).dt.hour

        tmp.rename(columns=lambda x: x.strip().lower(), inplace=True)

        tmp2 = tmp.loc[((tmp["hour"] >= 0) &\
                       (tmp["hour"] < 5)) |\
                       (tmp["hour"] > 21)]

        tmp2["pickup_datetime"] = tmp["trip_pickup_datetime"]
        tmp2["pickup_longitude"] = tmp["start_lon"]
        tmp2["pickup_latitude"] = tmp["start_lat"]
        tmp2["dropoff_datetime"] = tmp["trip_dropoff_datetime"]
        tmp2["dropoff_longitude"] = tmp["end_lon"]
        tmp2["dropoff_latitude"] = tmp["end_lat"]
        tmp2["passenger_count"] = tmp["passenger_count"]
        
        tmp3 = tmp2[["pickup_datetime",\
                     "pickup_longitude",\
                     "pickup_latitude",\
                     "dropoff_datetime",\
                     "dropoff_longitude",\
                     "dropoff_latitude",\
                     "passenger_count"]]


        tmpStr = 'tripdata_{:4d}-{:02d}.hdf'.format(i,j)
        tmp3.to_hdf('../Data/{:s}'.format(tmpStr),'table')
        
        del tmp
        del tmp2
        del tmp3
        gc.collect()
    


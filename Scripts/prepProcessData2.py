import pandas as pd
import gc

for i in [2015,2016]:
    for j in range(1,13):
        print(i,j)
        PATH = "../Raw_Data/yellow_tripdata_{:4d}-{:02d}.csv.gz".format(i,j)
        tmp = pd.read_csv(PATH,\
                          engine='c',\
                          error_bad_lines=False)

        tmp.rename(columns=lambda x: x.strip().lower().replace('lpep_','').replace('tpep_',''), inplace=True)

        print([tmp.columns])

        tmp["hour"] = pd.to_datetime(tmp["pickup_datetime"],\
                                     format="%Y/%m/%d %H:%M:%S",\
                                     errors='ignore',\
                                     box=True).dt.hour

        tmp2 = tmp.loc[((tmp["hour"] >= 0) &\
                        (tmp["hour"] < 5)) |\
                       (tmp["hour"] > 21)]

        tmp2["pickup_datetime"] = tmp["pickup_datetime"]
        tmp2["pickup_longitude"] = tmp["pickup_longitude"]
        tmp2["pickup_latitude"] = tmp["pickup_latitude"]
        tmp2["dropoff_datetime"] = tmp["dropoff_datetime"]
        tmp2["dropoff_longitude"] = tmp["dropoff_longitude"]
        tmp2["dropoff_latitude"] = tmp["dropoff_latitude"]
        tmp2["passenger_count"] = tmp["passenger_count"]
        
        tmp3 = tmp2[["pickup_datetime",\
                     "pickup_longitude",\
                     "pickup_latitude",\
                     "dropoff_datetime",\
                     "dropoff_longitude",\
                     "dropoff_latitude",\
                     "passenger_count"]]

########################################

        PATH2 = "../Raw_Data/green_tripdata_{:4d}-{:02d}.csv.gz".format(i,j)
        tmp4 = pd.read_csv(PATH2,\
                          engine='c',\
                          error_bad_lines=False)

        tmp4["hour"] = pd.to_datetime(tmp4["pickup_datetime"],\
                                     format="%Y/%m/%d %H:%M:%S",\
                                     errors='ignore',\
                                     box=True).dt.hour

        tmp4.rename(columns=lambda x: x.strip().lower().replace('lpep_','').replace('tpep_',''), inplace=True)

        tmp5 = tmp4.loc[((tmp4["hour"] >= 0) &\
                        (tmp4["hour"] < 5)) |\
                       (tmp4["hour"] > 21)]

        tmp5["pickup_datetime"] = tmp4["pickup_datetime"]
        tmp5["pickup_longitude"] = tmp4["pickup_longitude"]
        tmp5["pickup_latitude"] = tmp4["pickup_latitude"]
        tmp5["dropoff_datetime"] = tmp4["dropoff_datetime"]
        tmp5["dropoff_longitude"] = tmp4["dropoff_longitude"]
        tmp5["dropoff_latitude"] = tmp4["dropoff_latitude"]
        tmp5["passenger_count"] = tmp4["passenger_count"]
        
        tmp6 = tmp5[["pickup_datetime",\
                     "pickup_longitude",\
                     "pickup_latitude",\
                     "dropoff_datetime",\
                     "dropoff_longitude",\
                     "dropoff_latitude",\
                     "passenger_count"]]

        tmpStr = 'tripdata_{:4d}-{:02d}.hdf'.format(i,j)

        tmp7 = pd.concat([tmp3,tmp6])
        tmp7.to_hdf('../Data/{:s}'.format(tmpStr),'table')

        del tmp
        del tmp2
        del tmp3
        del tmp4
        del tmp5
        del tmp6
        del tmp7
        gc.collect()
    


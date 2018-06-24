#!/bin/bash
echo "" >> time.log
for i in `seq -w 2009 2012`
do
    for j in `seq -w 01 12`
    do
	echo "Processing: $i $j" &>> time.log
	wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_$i-$j.csv
	time `pigz yellow_tripdata*.csv` &>> time.log
    done
done

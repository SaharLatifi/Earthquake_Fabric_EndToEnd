# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "51ab4df0-9729-4175-a0f4-6eff16f4f359",
# META       "default_lakehouse_name": "earthquake_lh",
# META       "default_lakehouse_workspace_id": "c8be695d-7165-4282-a37f-f28f6fea60ec"
# META     }
# META   }
# META }

# MARKDOWN ********************

# ## Worldwide Earthquake Events API 
# ### Ingest data into lakehouse (Bronze Layer)


# CELL ********************

import requests
import json


from datetime import date,timedelta

start_date = "2014-01-08"
end_date = "2014-01-12"



start_date = date.today() - timedelta(7)
end_date = date.today() - timedelta(1)


# Build the API URL using string formatting and the specified start/end dates provided by Data Factory
url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"
#url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02"

# Get Request to fetch the data from using API


status_code = requests.get(url).status_code

# Check if the get request was successfull
if status_code != 200:
    raise Exception(f"API request failed with status code {response.status_code}")

response = requests.get(url)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************



from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType,TimestampType
from pyspark.sql.functions import col ,from_unixtime

quake_schema = StructType([
    StructField("id", StringType(), True),
    StructField("magnitude", DoubleType(), True),  # force double
    StructField("place", StringType(), True),
    StructField("time", DoubleType(), True),         # if you want time as a long
    StructField("longitude", DoubleType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("depth", DoubleType(), True)
])

 # Specify the destination file name and path
file_path = "Files/earthquake_data"


# Get the JSON data 
data_quake = response.json()


# Extract the "features" key from the JSON.
# This key holds an array (list) where each element is a dictionary describing one earthquake event.
data_quake_features = data_quake['features']
#print(len(data_quake_features))

if not data_quake_features:
    raise Exception("No earthquake data found for the specified date range.")


# Loop over each item in the "features" list.
# Each item is a dictionary with keys like "id","properties", and "geometry    ".
records = []  # We'll store flattened quake data here

for feature in data_quake_features:
# Within each quake dictionary, read key-value pairs:
    quake_id = feature["id"]                    # or feature.get("id")
    quake_properties = feature["properties"]
    magnitude = quake_properties["mag"]         # or properties.get("time")
    place = quake_properties["place"]
    quake_time_ms = quake_properties["time"]  # ms since epoch
    quake_geometry = feature["geometry"]
    coordinates = quake_geometry["coordinates"]
    longitude, latitude, depth = coordinates[0], coordinates[1], coordinates[2]
    quake_time_s  = quake_time_ms / 1000.0 if quake_time_ms is not None else None

    magnitude = float(magnitude) if magnitude is not None else None
    #quake_time = float(quake_time) if quake_time is not None else None
    depth = float(depth) if depth is not None else None
    longitude = float(longitude) if longitude is not None else None
    latitude = float(latitude) if latitude is not None else None

    quake_data = {
        "id" : quake_id ,
        "magnitude" : magnitude ,
        "place" :place ,
        "time":quake_time_s,
        "longtitude":longitude,
        "latitude":latitude,
        "depth":depth
        }

    records.append(quake_data)

from collections import defaultdict

# Initialize a dictionary to hold the types for each field
type_dict = defaultdict(set)

# Iterate over each record and collect types
for record in records:
    for key, value in record.items():
        type_dict[key].add(type(value))

# Identify fields with multiple types
for key, types in type_dict.items():
    #print(types)
    if len(types) > 1:
        print(f"Field '{key}' has multiple types: {types}")

quake_df = spark.createDataFrame(records,schema=quake_schema)
quake_df = quake_df.withColumn("time_stamp" , from_unixtime(col("time")).cast(TimestampType()))
quake_df = quake_df.withColumn("year" , col("time_stamp").substr(1,4)) \
                   .withColumn("month", col("time_stamp").substr(6,2)) \
                   .withColumn("day", col("time_stamp").substr(9,2))


quake_df.show(5)
quake_df.write.mode("append").partitionBy("year","month","day").parquet(file_path)


# for feature in data_quake_features:
#data_quake_features    


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.parquet("Files/earthquake_data/year=2014/month=01/day=04/part-00006-becad5ca-9287-44f9-91f1-0c9e05e7c7ff.c000.snappy.parquet")
# df now is a Spark DataFrame containing parquet data from "Files/earthquake_data/year=2014/month=01/day=04/part-00006-becad5ca-9287-44f9-91f1-0c9e05e7c7ff.c000.snappy.parquet".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

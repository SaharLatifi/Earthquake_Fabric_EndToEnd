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
# META       "default_lakehouse_workspace_id": "c8be695d-7165-4282-a37f-f28f6fea60ec",
# META       "known_lakehouses": [
# META         {
# META           "id": "51ab4df0-9729-4175-a0f4-6eff16f4f359"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ## Worldwide Earthquake Events API
# ### Ingest data into lakehouse (Bronze Layer)

# MARKDOWN ********************

# Worldwide Earthquake Events API
# Ingest data into lakehouse (Bronze Layer)

# CELL ********************

import requests
import json
import os 

from datetime import date,timedelta

#start_date = date.today() - timedelta(1)
#end_date = date.today() - timedelta(1)


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

quake_data = response.json()
quake_data_features = quake_data["features"]

 
file_path = f"/lakehouse/default/Files/{start_date}earthquake_data.json"

directory = os.path.dirname(file_path)

# if the file doesw not exists it will create it and if exists it will be overwritted
with open(file_path,'w') as file:
    json.dump(quake_data_features,file,indent=4)

#print(f"Data successfully saved to {file_path}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.option("multiline", "true").json(f"Files/{start_date}earthquake_data.json")
# df now is a Spark DataFrame containing JSON data from "Files/earthquake_data.json".
#display(df)

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

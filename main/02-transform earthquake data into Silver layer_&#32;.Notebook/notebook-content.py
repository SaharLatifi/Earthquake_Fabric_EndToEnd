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
# ### Process data and transform into silver Layer

# CELL ********************

# -------------------------------
# Importing Required Libraries
# -------------------------------
# General PySpark modules
from datetime import date , timedelta 
from pyspark.sql.types import StructType,StructField,IntegerType, DoubleType,StringType , ArrayType , LongType , TimestampType
from pyspark.sql.functions import col, explode_outer , size

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# -------------------------------
# Variable Settings
# -------------------------------

##start_date = date.today() - timedelta(7)
##end_date = date.today() - timedelta(1)

file_path = f"Files/{start_date}earthquake_data.json"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Step 1 - Read the JSON file from the lakehouse into a DataFrame
df_earth_quake = spark.read.option("multiline", "true").json(file_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ToDo: Remove this code after debugging and verifying the code. (This code is for learning and verifying functionality, unrelated to the business logic
df_earth_quake.columns[2]
#display(df_earth_quake.select(col('geometry')['coordinates'][1]))
#display(df_earth_quake.select(col('geometry.coordinates')[1]))
display(df_earth_quake.select(col('geometry.coordinates').getItem(0)))
display(df_earth_quake.select(col('properties')['mag']))
#display(df_earth_quake.select(df_earth_quake.columns[2]))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

# Step 2 - Define a function to expand and flatten the JSON file
# This includes unpacking nested structures like arrays and dictionaries

def expand_json (df):
    expanded_df = df
    complex_fields = {field.name : field.dataType
    for field in df.schema.fields
    if isinstance(field.dataType,(StructType,ArrayType))}

# Unpack all the array or struct data types
    for key , value in complex_fields.items():
        if isinstance(value,ArrayType):
            array_size = df.select(size(col(key)).alias("size")).first()["size"]
            #print(array_size)
            for i in range(array_size):
                expanded_df = expanded_df.withColumn(f"{key}_{i}" , col(key)[i])
            #print(key)
            expanded_df.drop(key)
        elif isinstance(value,StructType):
            expanded = [col(f"{key}.{field.name}").alias(f"{key}_{field.name}")
            for field in value]
            #print(key)
            #print(expanded)
            expanded_df = expanded_df.select("*",*expanded).drop(key)
    return expanded_df

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Step 3 - Call the function to flatten the JSON DataFrame
# This step also includes:
# - Adding latitude (`lat`), longitude (`lon`), and length (`len`) from nested fields
# - Expanding the `properties` dictionary into separate columns

# Expand the struct types
df_earth_quake_flattened = expand_json(df_earth_quake)

# Expand the array types
df_earth_quake_flattened = expand_json(df_earth_quake_flattened)

# Convert the time  and updated column from unix time (in milliseconds) to a human readable timestampe
df_earth_quake_final = df_earth_quake_flattened.select(
                        col("id").alias("earquake_id"),
                        col("geometry_coordinates_0").alias("long"),
                        col("geometry_coordinates_1").alias("lat"),
                        col("geometry_coordinates_2").alias("elevation"),
                        col("properties_title").alias("title"),
                        col("properties_place").alias("place_description"),
                        col("properties_sig").alias("sig"),
                        col("properties_mag").alias("mag"),
                        col("properties_magType").alias("mag_type"),
                        (col("properties_time")/1000).cast(TimestampType()).alias("time"),
                        (col("properties_updated")/1000).cast(TimestampType()).alias("updated")
                        )



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_earth_quake_final.write.mode("append").saveAsTable("earthquake_events_silver")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# -------------------------------
# Clean Up
# -------------------------------
#spark.stop()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

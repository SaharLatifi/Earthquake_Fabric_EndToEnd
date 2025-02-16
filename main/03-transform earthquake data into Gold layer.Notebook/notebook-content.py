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
# META     },
# META     "environment": {
# META       "environmentId": "e23fd9a3-fd1a-9629-42d7-cd1ce63e968f",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# CELL ********************

# -------------------------------
# Importing Required Libraries
# -------------------------------
# General PySpark modules
from pyspark.sql.types import StringType
from pyspark.sql.functions import when,col,udf,lit
# First ensure the below library is installed on the Fabric environment
import reverse_geocoder as rg 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_earth_quake = spark.read.table("earthquake_events_silver").filter(col('time') >start_date)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Retrieve the ISO country code for a given latitude and longtitude.
def get_country_code(lat, lon):
    coordinates = (float(lat), float(lon))
    return rg.search(coordinates)[0].get('cc')

get_country_code_udf = udf(get_country_code)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_earth_quake_with_location = df_earth_quake.withColumn("country_code" , get_country_code_udf(col("lat"),col("long")))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_earth_quake_with_location_sig_class = df_earth_quake_with_location. \
                   withColumn('sig_class' ,
                        when(col("sig") < 100 , "Low").\
                        when((col("sig") >=100 )  & (col("sig") < 500 ) , "Moderate").\
                        otherwise("High")
                       ) 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Appending the data to the Gold layer table
df_earth_quake_with_location_sig_class.write.mode("append").saveAsTable("earthquake_events_gold")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************


# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

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

# CELL ********************

# Importing required libraries
from pyspark.sql.functions import col , to_date

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# PARAMETERS CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
# Defining variables
start_date = '2025-01-01'
end_date = '2025-01-20'
country_code = 'CA'
place_description = 'Osoyoos'

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read all the events happend in Canada during the time frame 
eq_df = spark.read.table("earthquake_events_gold").filter(
        (col("country_code") ==country_code)   &
        (to_date(col('time')).between(start_date,end_date) &
        col("place_description").contains(place_description)) 
      )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

if eq_df.count() != 0:
    start_date_replace_hyphen = start_date.replace("-","_")
    tabel_name = f"{place_description}_events_{start_date_replace_hyphen}"
    print(tabel_name)
    eq_df.write.mode("append").saveAsTable(tabel_name)
    #df_earth_quake_with_location_sig_class.write.mode("append").saveAsTable("earthquake_events_gold")

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

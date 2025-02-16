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
from pyspark.sql.functions import col , to_date , avg , max , count

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Defining variables
start_date = '2025-01-01'
end_date = '2025-01-20'
country_code = 'CA'

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# 1.  <mark><mark></mark></mark>How many earthquake happened in Canada in the first 2o days of the year?
# 1. What is the average magnitude?
# 1.  Where did the strongest earthquake happened?
# 1.  Was there any earthquake in Whistler?
# 1. Was there any earthquake in Osoyoos?
# 1. What was the trend in the first 20 days of the year? 

# CELL ********************

# Read all the events happend in Canada during the time frame 
eq_df = spark.read.table("earthquake_events_gold").filter(
        (col("country_code") ==country_code)   &
        (to_date(col('time')).between(start_date,end_date)) 
      )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Question1: How many earthquake happened in Canada in the first 2 weeks of Jan 2025?
print(f"{eq_df.count()} earthquake happend in Canada from {start_date} to {end_date}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Question2: What is the average magnitude?
average_mag_df = eq_df.agg(avg("mag").alias("average_magnitude"))
average_mag = average_mag_df.first()[0]
print(f"The average magnitude was {average_mag}") 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Question3: Where did the strongest earthquake happened?
max_mag = eq_df.agg(max("mag").alias("max_magnitude")).first()[0]
location_with_max_mag = eq_df.filter(col("mag") == max_mag).select("place_description").distinct().first()[0]
print(f"The maximum mag was {max_mag}")
display(location_with_max_mag)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Question4: Was there any earthquake in Whistler?
whistler_eq_df = eq_df.filter(
    col("place_description").contains("Whistler")
)
if whistler_eq_df.count() != 0:
    print(f"{whistler_eq_df.count()} earthquakes happend in Whistler during {start_date} and {end_date}")
else:
    print(f"No earthquake happend in Whistler during {start_date} and {end_date}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Question4: Was there any earthquake in Osoyoos?
osoyoos_eq_df = eq_df.filter(
    col("place_description").contains("Osoyoos")  
)
if osoyoos_eq_df.count() != 0:
    print(f"{osoyoos_eq_df.count()} earthquakes happend in Osoyoos during {start_date} and {end_date}")
else:
    print(f"No earthquake happend in Osoyoos during {start_date} and {end_date}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

eq_df_agg = eq_df.groupBy(to_date(col("time"))).agg(count("*").alias("number_of_earthquake"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 6.What was the trend in the first 20 days of the year?
display(eq_df_agg)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import seaborn as sns
import matplotlib.pyplot as plt

pandas_df = eq_df_agg.toPandas()

plt.figure(figsize=(10,6))
sns.lineplot(data=pandas_df,x="to_date(time)", y="number_of_earthquake" , marker ="o")

plt.title("Number of Earthquakes Per Day" , fontsize =16)
plt.xlabel("Date", fontsize =12)
plt.ylabel("Number of Earthquakes Per Day", fontsize = 12)
plt.xticks(rotation = 45)
plt.grid(visible=True)

plt.show()

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

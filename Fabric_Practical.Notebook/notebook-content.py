# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "48e0a0e6-d4a3-4b3e-a5e3-7ccaffa0d1e2",
# META       "default_lakehouse_name": "Fabric_Lakehouse",
# META       "default_lakehouse_workspace_id": "2ff589e8-6b79-4bdf-ba88-1f2d730b59a9",
# META       "known_lakehouses": [
# META         {
# META           "id": "48e0a0e6-d4a3-4b3e-a5e3-7ccaffa0d1e2"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# %%html
# # **Data Engineer 1**


# CELL ********************

df = spark.read.format("csv").option("header","true").load("Files/Raw_Data/AdventureWorks_Customers_parameter.csv")
# df now is a Spark DataFrame containing CSV data from "Files/Raw_Data/AdventureWorks_Customers_parameter.csv".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM Fabric_Lakehouse.dbo.customer_data_1 LIMIT 1000")
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

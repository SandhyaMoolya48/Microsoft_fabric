# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "878c8a65-00b6-41e2-9ced-f056be36f2df",
# META       "default_lakehouse_name": "Silver_Lakhouse",
# META       "default_lakehouse_workspace_id": "2ff589e8-6b79-4bdf-ba88-1f2d730b59a9",
# META       "known_lakehouses": [
# META         {
# META           "id": "878c8a65-00b6-41e2-9ced-f056be36f2df"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import *

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# 
# # **Reading Shortcuts**


# CELL ********************

df=spark.read.format("csv").option("header",True).load("Files/Raw_DataAdventureWorks_Customers/AdventureWorks_Customers.csv")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # **Reading Bronze Lakehouse data**

# MARKDOWN ********************

# ### **Read the customer data**

# CELL ********************

df1=spark.read.format("CSV")\
         .option("header",True)\
         .option("inferSchema",True)\
         .load("abfss://Fabric_Practical@onelake.dfs.fabric.microsoft.com/Fabric_Lakehouse.Lakehouse/Files/Raw_DataAdventureWorks_Customers") 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df1.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df1)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df1=df1.withColumn("fullname",concat(col('Prefix'),lit(" "),col('FirstName'),lit(" "),col('LastName')))
display(df1)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

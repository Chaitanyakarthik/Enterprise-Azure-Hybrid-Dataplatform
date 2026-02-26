# Databricks notebook source
from pyspark.sql.functions import sum, col, when

# COMMAND ----------


from pyspark.sql.functions import sum, col, when
spark.conf.set("fs.azure.account.key.enterprisestorage77.blob.core.windows.net",dbutils.secrets.get(scope="databricks scope",key="secretkv"))

# COMMAND ----------

dbutils.secrets.listScopes()


# COMMAND ----------

spark.conf.set("fs.azure.account.key.enterprisestorage77.blob.core.windows.net",dbutils.secrets.get(scope="databricks scope", key="secretkv"))

# COMMAND ----------

dbutils.fs.ls("wasbs://raw-data@enterprisestorage77.blob.core.windows.net/")

# COMMAND ----------

accounts_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("wasbs://raw-data@enterprisestorage77.blob.core.windows.net/accounts.csv")

accounts_df.display()

# COMMAND ----------

products_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("wasbs://raw-data@enterprisestorage77.blob.core.windows.net/products.csv")
display(products_df)

# COMMAND ----------

pipeline_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("wasbs://raw-data@enterprisestorage77.blob.core.windows.net/sales_pipeline.csv")

display(pipeline_df)

# COMMAND ----------

teams_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("wasbs://raw-data@enterprisestorage77.blob.core.windows.net/sales_teams.csv")

display(teams_df)

# COMMAND ----------

dictionary_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("wasbs://raw-data@enterprisestorage77.blob.core.windows.net/data_dictionary.csv")

display(dictionary_df)

# COMMAND ----------

print(accounts_df.columns)
print(products_df.columns)
print(pipeline_df.columns)
print(teams_df.columns)
print(dictionary_df.columns)

# COMMAND ----------

accounts_df = accounts_df.withColumnRenamed("subsidiary_of", "parent_company")

dictionary_df = dictionary_df \
    .withColumnRenamed("Table", "table") \
    .withColumnRenamed("Field", "field") \
    .withColumnRenamed("Description", "description")

accounts_df.show(1)
dictionary_df.show(1)

# COMMAND ----------

null_counts_accounts_df = accounts_df.select([sum(when(col(column).isNull(), 1).otherwise(0)).alias(column) for column in accounts_df.columns])

null_counts_dictionary_df = dictionary_df.select([sum(when(col(column).isNull(), 1).otherwise(0)).alias(column) for column in dictionary_df.columns])

null_counts_products_df = products_df.select([sum(when(col(column).isNull(), 1).otherwise(0)).alias(column) for column in products_df.columns])

null_counts_pipeline_df = pipeline_df.select([sum(when(col(column).isNull(), 1).otherwise(0)).alias(column) for column in pipeline_df.columns])

null_counts_teams_df =teams_df.select([sum(when(col(column).isNull(), 1).otherwise(0)).alias(column) for column in teams_df.columns])

# COMMAND ----------

null_counts_accounts_df.display()

# COMMAND ----------

null_counts_dictionary_df.display()
null_counts_products_df.display()
null_counts_pipeline_df.display()
null_counts_teams_df.display()

# COMMAND ----------

pipeline_df.display()

# COMMAND ----------

accounts_df = accounts_df.fillna({"parent_company": "Independent"})

pipeline_df = pipeline_df.fillna({"account": "Unknown"})

# COMMAND ----------

accounts_df.display()

# COMMAND ----------

pipeline_df.show()

# COMMAND ----------

null_counts_accounts_df = accounts_df.select([sum(when(col(column).isNull(), 1).otherwise(0)).alias(column) for column in accounts_df.columns])

accounts_df.display()

# COMMAND ----------

null_counts_accounts_df.display()

# COMMAND ----------

accounts_df.write.mode("overwrite").parquet(
    "abfss://transformed-container@enterprisestorage77.dfs.core.windows.net/"
)

# COMMAND ----------

dbutils.secrets.get(scope="databricks scope", key="secretkv")

# COMMAND ----------

spark.conf.set(
  "fs.azure.account.key.enterprisestorage77.dfs.core.windows.net",
  dbutils.secrets.get(scope="databricks scope", key="secretkv")
)

# COMMAND ----------

accounts_df.write.format("delta").mode("overwrite").save(
    "abfss://transformed-container@enterprisestorage77.dfs.core.windows.net/"
)

# COMMAND ----------

dictionary_df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("abfss://transformed-container@enterprisestorage77.dfs.core.windows.net/data_dictionary/")

# COMMAND ----------

products_df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("abfss://transformed-container@enterprisestorage77.dfs.core.windows.net/products/")

# COMMAND ----------

pipeline_df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("abfss://transformed-container@enterprisestorage77.dfs.core.windows.net/sales_pipeline/")

# COMMAND ----------

teams_df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("abfss://transformed-container@enterprisestorage77.dfs.core.windows.net/sales_teams/")

# COMMAND ----------


from pyspark.sql import SparkSession
from pyspark.sql.functions import concat_ws

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Concatenate Names") \
    .getOrCreate()

# Define schema for the flat file
schema = "First_Name STRING, Last_Name STRING"

# Load the flat file into a DataFrame from S3
file_path = "s3://step2function/input/names.csv"  
names_df = spark.read.csv(file_path, header=True, schema=schema)

# Concatenate first and last names into a full name
full_names_df = names_df.withColumn("Full_Name", concat_ws(" ", names_df.First_Name, names_df.Last_Name))

# Show the result
full_names_df.show()

# Optionally, write the result back to S3 with overwrite mode
output_path = "s3://step2function/output/" 
full_names_df.write.mode("overwrite").csv(output_path, header=True)

# Stop the SparkSession
spark.stop()
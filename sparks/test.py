from pyspark.sql import SparkSession

# Create a Spark session (which will start a Spark application)
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("TestApp") \
    .getOrCreate()

# Create a DataFrame to ensure Spark is working
data = [("Java", 20000), ("Python", 100000), ("Scala", 3000)]
df = spark.createDataFrame(data, ["Language", "Users"])

# Show the DataFrame
df.show()

# Stop the Spark session
spark.stop()

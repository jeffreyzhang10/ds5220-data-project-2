import os
import requests
import pandas as pd
import boto3
import matplotlib.pyplot as plt
from datetime import datetime
from io import StringIO

# env vars
S3_BUCKET = os.environ["S3_BUCKET"]
S3_DATA_KEY = os.environ["S3_DATA_KEY"]
S3_PLOT_KEY = os.environ["S3_PLOT_KEY"]
AWS_REGION = os.environ["AWS_REGION"]

# S3 CLIENT
s3 = boto3.client("s3", region_name=AWS_REGION)

# charlottesville coords 
LAT = 38.03
LON = -78.48

# api HERE
url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
response = requests.get(url)
data = response.json()

# EXTRACT WEATHER
current_weather = data["current_weather"]

new_row = {
    "timestamp": datetime.utcnow().isoformat(),
    "temperature": current_weather["temperature"],
    "windspeed": current_weather["windspeed"]}

new_df = pd.DataFrame([new_row])

# load data from S3 (if exists)
try:
    obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_DATA_KEY)
    df = pd.read_csv(obj["Body"])
    print("Loaded data from S3")
except:
    df = pd.DataFrame()
    print("No data found. ")

# make df
df = pd.concat([df, new_df], ignore_index=True)

# save as instructed 
df.to_csv("data.csv", index=False)

# upload data to S3
s3.upload_file("data.csv", S3_BUCKET, S3_DATA_KEY)
print("Uploaded data.csv to S3")

# create plot.png
plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["temperature"])
plt.xticks(rotation=45)
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Charlottesville, VA Temperature Over Time")
# plt.tight_layout()

# save plot 
plt.savefig("plot.png")

# up plot to s3
s3.upload_file("plot.png", S3_BUCKET, S3_PLOT_KEY)
print("Uploaded plot.png to S3")
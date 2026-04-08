# Data Source Summary 

In this DS5220 Project, I am using data from Open Meteo's weather forecast API. As I was sitting outside on the lawn below the Rotunda, it was a particularly nice day out which saw students, tourists, and locals alike creating a really positive atmosphere around Grounds. To me personally, there is really nothing better than mid 70's weather with a slight breeze. Nonetheless, I decided to look at weather data in Charlottesville, just to be able to visualize how changes in weather might look, especially over this week, since it would be significantly cooler. Within the data itself, I am looking specifically at temperature and windspeed because of how nice it was, and analyzing changes over time. 

# Scheduled Process

With the process for my data application, I deployed a containerized Python script that sits on a cronJob Kubernetes schedule. I configured the process to run once every hour for 72 hours in order to collect 72 data points over the span of three days. Every hour, the application sends a requst to the Open Mateo API, extracting relevant variables like temperature. Then, the application adds the information to a data set stored in S3. Then, the data is preserved and regenerated for plots and visualizations. 

# Data Description and Analysis 

As part of the requirements for the assignment, I had to include an output data set and plot. 

## data.csv 
A cumalative dataset containing observations on weather patterns, including time, temperature and windspeed. Each row represents the snapshot of the weather at an hourly interval. 

## plot.png
A cumulative visualization based on the above dataset, which shows how temperature fluctuates over time, over the day, as well as over the aforementioned 72-hour period. 

## Observations 

Over the 72-hour period, the data and plot showed significant, but logically reasonable fluctuations in temperature throughout the day. Tempereatures were rose and were higher throughout the day and into the afternoon, but as the sun went down in the evening and into the night, temperatures tended to hit their lows. Given temperature fluctuations that mirror what I would have expected, general patterns persisted and did not have any surprises. One other thing to note, as discussed with Professor Mcgee in class, is the absence of several points on the morning of April 7th for a period spanning a couple hours. This could be due to a variety of factors, such a temporary downtime for the API itself. As a result, it would be worth looking into the logs of the application to see what types of errors are present, especially as considering this in a production setting, this would be of major concern. 

## Discussion 

* How Kubernetes Secrets differ from plain environment variables and why that distinction matters.

Kubernetes secrets differ from environment variables due to the information that they hold. The secrets hold sensitive information that you do not want out there, like API keys, while environment variables hold information that are specific but do not need to be held separately from the code to avoid being pushed and leaked on Github. 

* How your CronJob pods gain permission to read/write to AWS services without credentials appearing in any file.

My CronJob gets its permissions from the IAM role that I attached to the EC2 instance at the beginning of the project. As a result, AWS gives credentials to the isntance which is thus by extension applied to the applications inside my container. This is what allows the CronJob to read and write to S3 without any access keys, which is simpler and easier. 

* One thing you would do differently if you were building this pipeline for a real production system.

One thing I'd focus on in production is upgrading from S3 csv files to something like parquet. Right now, looking only at one variable over time is easy to manage, and not really a problem. However, in the real world, with models that require significantly more information and variables int he dataset. Using a parquet file is more efficient, makes these systems more scalable and manageable, and allows me to focus such an application on getting the information needed to solve real world business problems. 





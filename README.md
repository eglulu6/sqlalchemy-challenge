# SQLAlchemy Challenge
---
**Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.**

## Step 1 - Climate Analysis and Exploration

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Use SQLAlchemy to connect to your sqlite database.

* Use SQLAlchemy to reflect your tables into classes.

* Link Python to the database.

### Precipitation Analysis

* Start by finding the most recent date in the data set.

* Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data. **Note** you do not pass in the date as a variable to your query.

* Load the query results into a Pandas DataFrame.

* Plot the results.

* Print the summary statistics for the precipitation data.

### Station Analysis

* Design a query to calculate the total number of stations in the dataset.

* Design a query to find the most active stations.

  * Calculate the lowest, highest, and average temperature of the most active stations.
  
* Design a query to retrieve the last 12 months of temperature observation data (TOBS) from the most active station.

  * Plot the results as a histogram.

- - -

## Step 2 - Climate App

Design a Flask API based on the queries that you have just developed.

### Routes

* `/`  Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation` Precipitation Analysis of the last 12 months

  * Convert the Precipitation Analysis query results to a dictionary.

* `/api/v1.0/stations` Station Analysis for all stations precipitation 

  * Convert the Station Analysis query results of all stations precipitation

* `/api/v1.0/tobs` Station Analysis for most active station temp observations

  * Query the dates and temperature observations of the most active station for the last year of data.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`  Temperature Analysis of all temps within a specified period

  * When given the start only, calculate the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the minimum temperature, the average temperature, and the max temperature for dates between the start and end date inclusive.

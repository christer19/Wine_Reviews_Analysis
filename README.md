# Overview

The goal of this project is to create a tool that presents the information from the wine magazine reviews data, in a easy and interactive manner using different types of vizualizations to explorer the data.

# Resources Used

- Python version 3.8.3.
    - Data processing libraries: numpy, pandas and nltk.
    - Visualization libraries: bokeh, hvplot, PIL and WordCloud.
    - Dashboard design library: Panel 0.9.7
    - Other supporting libraries: matplotlib and seaborn
    
    
- Images for this project taken from: https://pixabay.com/vectors/search/wine/
- Other data used: Grapes variety was obtained from https://en.wikipedia.org/wiki/List_of_grape_varieties
- Credits to Doung Vu for [Generating WordClouds in Python.](https://www.datacamp.com/community/tutorials/wordcloud-python)


# Project Steps:
## Data Collection
The data comes from a csv file containing the information of 130,000 reviews of wines, from [The Wine Enthusiast Magazine.](https://www.winemag.com/) This data was scraped during the week of June 15th 2017 by [Zack Thoutt.](https://github.com/zackthoutt/wine-deep-learning) For each reviewed wine it includes country, description(taster review), designation, points or rating, price, province, regions, taster name, title, variety and winery.


## Data Cleaning
In order to simplify the analysis and to guarantee a better quality of the data. It was transformed by replacing or removing missing values, creating new columns (feature engineering) from the pre-existing ones and removing some of the columns that were considered not relevant for this project.

## Data Exploration

## Dashboard App Deployment

    
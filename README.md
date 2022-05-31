# Project 4 - Housing Price

flask - app.py
 -connects to postgresql or sqlite. 
 - initial load can be run locally by running "/load"
   file ml_script.py: 
    * takes the 3 csv's with housing pricing, county GDP and censue income data
    * cleans data, merge dataframes, covert the dataframes to the appropriate format for unsupervised (clustering) and supervised (linear regression) machine learning.
    * output is saved to sql database (using  sqlalchemy)(+24,000 rows). Runs with local postgres or SQLite. Exceeds Heroku Postgress limit for free plan.
 - flask reads data from database and creates displays on two html pages (supervised and unsupervised ML) using plotly and js
 - links provided to Tableau visualizations using Tableau Public links
   

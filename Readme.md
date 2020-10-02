Summary of the Project 

A) Purpose and Analytical Goals

1. Music streaming company ‘Sparkify’ currently have all their data stored in a directory of JSON logs on AWS S3 and therefore there is no easy way 
   to query their data so the purpose of this project is to store the data from these JSON files into Redshift database so the 
   data can be queried efficiently through optimized sql queries.
   
2. Major analytical goal of the company is to get a better understanding of the kinds of songs the users are currently listening to as well 
   as the artists that they are following on the music streaming app. 

B) Database Schema design and ETL pipeline.

1. The database schema consists of new database called 'sparkify' which contains 1 fact table and 4 dimension tables as shown below along   
   with their column names. 

a. Fact Table
     songplays - records in log data associated with song plays i.e. records with page NextSong
     columns : songplay_id, start_time, user_id, level, song_id, artist_id, session_id,location, user_agent 

b. Dimension Tables
     users - contains all the users in the music streaming app
     columns : user_id, first_name, last_name, gender, level
     songs - contains all the songs in the music streaming app 
     columns : song_id, title, artist_id, year, duration
     artists - contains all the artists in the music streaming app
     columns : artist_id, name, location, latitude, longitude
     time - timestamps of records in songplays fact table broken down into specific units
     columns : start_time, hour, day, week, month, year, weekday
     
2. ETL pipeline transfers data from JSON files in AWS S3(s3://udacity-dend/log_data and s3://udacity-dend/song_data) into the above tables in     
   Redshift database using Python Code and SQL Queries.
   
3. ETL consists of below 3 python files which is present in the repository. 
   1.sql_queries.py - this file contains all the sql queries to drop/create as well as insert data into the 2 staging tables as well as 4 
                      dimensions and 1 fact table. 
   2.create_tables.py - this file contains 2 functions which is called by the main() function in the same order as shown below  
     a.main() - function is called to connect to the Redshift database in Amazon Web Services(AWS).
     b.drop_tables(cur, conn)- function is called to drop the tables.
     c.create_tables(cur, conn) - function is called to create the tables.
   3.etl.py  - this is the main file to perform the ETL and consists of the below 2 functions. 
     a. load_staging_tables(cur, conn) - function extracts the data from the files in AWS S3 and then loads the data into the 2 staging tables.
     b. load_final_tables(cur, conn) - function loads the data from the 2 staging tables into the final analytical dimension/fact tables.
4. Please follow the below 2 steps in the same order to perform the entire ETL. 
    a. Open the terminal and run the below command to drop/create all the tables.
       Command : python3 create_tables.py
    b. Run the below command to load the data from the JSON files in AWS S3 into the staging tables and then from staging into the final analytical        dimension/fact tables. 
       Command : python3 etl.py
       
   

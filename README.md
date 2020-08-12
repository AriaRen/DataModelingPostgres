# Data Modeling Postgres
Description: Create a Postgres database with tables designed to optimize queries on song play analysis for a startup called Sparkify.

## Purpose of SongPlay Database
The purpose of this database is getting a convenient way to query data for their analytical process. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Database Schema Design
In computing, the star schema is the simplest style of data mart schema and is the approach most widely used to develop data warehouses and dimensional data marts. In this case, I created one fact table, songplays, to reference other 4 dimension tables: users, songs, artists, time. Based on the schema design, I wrote python script to create one Postgres SQL database and 5 tables. 

## ETL Pipeline Description
etl.py includes the whole process including pulling JSON files from certain directories (Basically 2 data sources), selected only the variables what analytic team wants for database and extract one by one to tables we already created. 

## How to run Python Scripts
To properly create database and have all data stored, the user should firstly have all scripts on hand: sql_queries.py, create_tables.py and etl.py. Then, run create_tables.py to finish building the database structure and lastly etl.py to get all data ready! Finaly, Sparkify gets its own Postgres SQL Database! 

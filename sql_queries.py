import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "drop table if exists staging_events"
staging_songs_table_drop = "drop table if exists staging_songs"
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

staging_events_table_create= ("""
create table staging_events(
artist varchar(510),
auth varchar(510),
firstName varchar(510),
gender varchar(510),
iteminSession varchar(510),
lastName varchar(510),
length varchar(510),
level varchar(510),
location varchar(510),
method varchar(510),
page varchar(510),
registration varchar(510),
sessionid varchar(510),
song varchar(510),
status varchar(510),
ts varchar(510),
userAgent varchar(510),
userid varchar(510)
)
""")

staging_songs_table_create = ("""
create table staging_songs(
num_songs varchar(510),
artist_id varchar(510),
artist_latitude varchar(510),
artist_longitude varchar(510),
artist_location varchar(510),
artist_name varchar(510),
song_id varchar(510),
title varchar(510),
duration varchar(510),
year varchar(510)
)
""")

user_table_create = ("""
create table users (
    user_id integer,
    first_name varchar(255),
    last_name varchar(255), 
    gender varchar(1) not null,
    level varchar(10) not null,
    primary key(user_id)
)diststyle auto
""")

song_table_create = ("""
create table songs (
    song_id varchar(25),
    title varchar(255),
    artist_id varchar(25) not null, 
    year integer not null,
    duration numeric not null,
    primary key(song_id)
)diststyle auto
""")

artist_table_create = ("""
create table artists (
    artist_id varchar(25), 
    name varchar(255) not null,
    location varchar(255), 
    latitude varchar(255),
    longitude varchar(255),
    primary key(artist_id)
)diststyle auto
""")

time_table_create = ("""
create table time (
    start_time bigint,
    hour integer not null,
    day integer not null, 
    week integer not null,
    month integer not null,
    year integer not null,
    weekday integer not null,
    primary key(start_time)
)diststyle auto
""")

songplay_table_create = ("""
create table songplays (
    songplay_id bigint identity(0,1),
    start_time bigint not null,
    user_id integer not null,
    song_id varchar(25),
    artist_id varchar(25),
    level varchar(10) not null,
    session_id integer not null,
    location varchar(255) not null,
    user_agent varchar(255) not null,
    primary key(songplay_id)
)diststyle auto
""")

# STAGING TABLES

staging_songs_copy = ("""copy staging_songs from 's3://udacity-dend/song_data/'
iam_role 'arn:aws:iam::687804185306:role/myRedshiftRole'
region 'us-west-2'
format as json 'auto'""")

staging_events_copy = ("""copy staging_events from 's3://udacity-dend/log_data/'
iam_role 'arn:aws:iam::687804185306:role/myRedshiftRole'
region 'us-west-2'
format as json 's3://udacity-dend/log_json_path.json'""")

# FINAL TABLES
 
user_table_insert = ("""
insert into users(user_id, first_name, last_name, gender, level)
select distinct userid::int,firstname,lastname,gender,level from staging_events
where userid != ''
order by userid::int asc
""")

song_table_insert = ("""
insert into songs(song_id,title,artist_id,year,duration)
select distinct song_id,title,artist_id,year::int,duration from staging_songs
""")

artist_table_insert = ("""
insert into artists(artist_id, name, location, latitude, longitude)
select distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude from staging_songs
""")

time_table_insert = ("""
insert into time(start_time,hour,day,week,month,year,weekday)
select distinct
a.start_time::bigint,
extract (hour from a.ts) as hour,
extract (day from a.ts) as day,
extract (week from a.ts) as week,
extract (month from a.ts) as month,
extract (year from a.ts) as year,
extract (weekday from a.ts) as weekday
from
(select ts as start_time,TIMESTAMP 'epoch' + ts/1000 *interval '1 second' as ts from staging_events) a
""")

songplay_table_insert = ("""
insert into songplays(start_time,user_id,level,song_id,artist_id,session_id,location,user_agent)
select e.ts::bigint,e.userid::int,e.level,s.song_id,a.artist_id,e.sessionid::int,e.location,e.useragent
from staging_events e
inner join songs s on e.song=s.title
inner join artists a on e.artist = a.name
where  page = 'NextSong'
""")
          
# QUERY LISTS

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]                   
create_table_queries = [staging_events_table_create,staging_songs_table_create,songplay_table_create,user_table_create,song_table_create,artist_table_create,
time_table_create]
copy_table_queries = [staging_songs_copy,staging_events_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert,songplay_table_insert]

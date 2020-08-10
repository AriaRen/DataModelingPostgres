import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import datetime


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[["song_id","title", "artist_id","year", "duration"]].values.tolist()[0]
    cur.execute(("INSERT INTO songs (song_id, title, artist_id, year, duration) \
                 VALUES (%s, %s, %s, %s, %s)"), song_data)
    
    # insert artist record
    artist_data = df[["artist_id","artist_name", "artist_location","artist_latitude", "artist_longitude"]].values.tolist()[0]
    cur.execute(("INSERT INTO artists (artist_id, name, location, latitude, longitude) \
                 VALUES (%s, %s, %s, %s, %s)"), artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page']=="NextSong",:]

    # convert timestamp column to datetime
    t = df.ts.apply(lambda x: datetime.datetime.fromtimestamp(x / 1e3))
    
    # insert time data records 
    time_df = pd.DataFrame({'ts':t, 'hour':pd.to_datetime(df.ts).dt.hour, 'day':pd.to_datetime(df.ts).dt.day,'week of year': pd.to_datetime(df.ts).dt.week, 'month':pd.to_datetime(df.ts).dt.month, 'year':pd.to_datetime(df.ts).dt.year, 'weekday':pd.to_datetime(df.ts).dt.weekday})

    for i, row in time_df.iterrows():
        cur.execute("INSERT INTO time (start_time, hour, day, week, month, year, weekday) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s)", list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute("INSERT INTO users (user_id, first_name, last_name, gender, level) \
                 VALUES (%s, %s, %s, %s, %s)", row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute("SELECT song_id, a.artist_id FROM songs s JOIN artists a ON s.artist_id=a.artist_id", (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (datetime.datetime.fromtimestamp(row.ts / 1e3), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute("INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
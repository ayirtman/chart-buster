#!/usr/bin/env python
# coding: utf-8

##### To scrap website

from bs4 import BeautifulSoup
import requests
import csv
import re
import pandas as pd
from yt_dlp import YoutubeDL


url = "https://top40weekly.com/1972-all-charts/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

data = []

# Find all p tags
p_tags = soup.find_all('p')

# Define the sections
sections = ["TW LW TITLE –•– Artist (Label)-Weeks on Chart (Peak To Date)", "THIS WEEK’S DROPS", "POWER PLAYS", "DEBUTS THIS WEEK"]

# Initialize the start index
start_index = 0

# Loop through the page until all sections have been processed
while start_index < len(p_tags):
    try:
        # Find the indices of the specific p tags
        start_index_1 = next(i for i, tag in enumerate(p_tags[start_index:]) if tag.text == sections[0]) + start_index
        end_index_1 = next(i for i, tag in enumerate(p_tags[start_index_1:]) if tag.text == sections[1]) + start_index_1

        start_index_2 = end_index_1
        end_index_2 = next(i for i, tag in enumerate(p_tags[start_index_2:]) if tag.text == sections[2]) + start_index_2

        start_index_3 = end_index_2
        end_index_3 = next(i for i, tag in enumerate(p_tags[start_index_3:]) if tag.text == sections[3]) + start_index_3

        # Get the p tags between the specific tags
        p_tags_between_1 = p_tags[start_index_1+1:end_index_1]
        p_tags_between_2 = p_tags[start_index_2+1:end_index_2]
        p_tags_between_3 = p_tags[start_index_3+1:end_index_3]

        # Print the text of the p tags, moving to a new line if a number in brackets is found
        for tag in p_tags_between_1 + p_tags_between_2 + p_tags_between_3:
            text = re.sub(r'\((\d+)\)', r'(\1)\n', tag.text)
            # Split the text on newlines and filter out any empty strings
            lines = [line for line in text.split('\n') if line]
            data.extend(lines)

        # Update the start index for the next iteration
        start_index = end_index_3 + 1

    except StopIteration:
        # If a StopIteration exception is raised, break the loop
        break

# Write the data to a CSV file
with open('songs.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Data"])
    for row in data:
        writer.writerow([row])

        

        
##### To rearrange the cells

# Read the csv file
df = pd.read_csv('songs.csv')

def parse_info(info):
    # Split the info based on the "–•–" delimiter
    parts = re.split(r'\s–•–\s', info)
    
    if len(parts) < 2:
        return pd.Series([None, None, None, None])  # return None values if the delimiter is not found
    
    # Get the song and artist names
    song_name = parts[0]
    artist_name = parts[1].split(' (')[0]  # split the artist_name on ' (' and take the first part
    
    # Further split the song_name to get this week's and last week's positions
    song_parts = song_name.split()
    
    # Check if there are at least three parts in song_parts (two positions and a song name)
    if len(song_parts) < 3:
        return pd.Series([None, None, None, artist_name])  # return None for the positions and song name if they are not found
    
    this_week_position = song_parts[0]
    last_week_position = song_parts[1]
    song_name = ' '.join(song_parts[2:])
    
    return pd.Series([this_week_position, last_week_position, song_name, artist_name])

# Apply the function to the 'info' column and create new columns
df[['This Week Position', 'Last Week Position', 'Song Name', 'Artist Name']] = df['Data'].apply(parse_info)

# Drop the original 'info' column (optional)
df = df.drop(columns=['Data'])

# Write the parsed data back to a new csv file (optional)
df.to_csv('parsed_chart_data.csv', index=False)



##### Download songs
def read_csv(file_path):
    df = pd.read_csv(file_path)
    num_rows = df.shape[0]
    return df, num_rows


def my_hook(d):
    if d['status'] == 'downloading':
        print(d['_percent_str'] + '\r', end='')
    elif d['status'] == 'finished':
        print()


def download_mp3(track, download_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': download_path + '/%(title)s.%(ext)s',
        'quiet': True,
        'progress_hooks': [my_hook],
        'ffmpeg_location': '/opt/homebrew/bin'  # Modify this line to your ffmpeg path
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'ytsearch:{track}'])


if __name__ == "__main__":
    file_path = 'parsed_chart_data.csv'
    download_path = '.'
    df, rows = read_csv(file_path)
    for index, row in df.iterrows():
        track = f"{row['Song Name']} {row['Artist Name']}"
        print(f"Downloading {index+1}/{rows}: {track}...")
        download_mp3(track, download_path)


# In[ ]:





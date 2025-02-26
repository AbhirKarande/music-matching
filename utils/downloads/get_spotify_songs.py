import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor
import os
import re

# You may decide on a custom downloads directory.
DOWNLOADS_DIR = os.getcwd()  # using the current directory

def is_duplicate(artist, song_title, download_dir):
    """
    Check if there is already a file named exactly "Artist - Song Title.mp3" in the download directory.
    Comparison is case-insensitive.
    """
    expected_filename = f"{artist} - {song_title}.mp3".lower()
    for filename in os.listdir(download_dir):
        if filename.lower() == expected_filename:
            return True
    return False

def download_url(line):
    """
    Given a line from spotify_urls_merged.txt, parse it to extract artist, song title, and the Spotify URL.
    The line is expected to be in the following format:
    
       <year><SEP><track_id><SEP><artist><SEP><song_title>    https://open.spotify.com/track/...
    
    It then checks for duplicate files based on the exact filename 'Artist - Song Title.mp3'
    and if no duplicate exists, downloads the song with spotdl.
    """
    if line.strip():
        # Use a regex to split the line into metadata and the url.
        match = re.match(r'^(.*?)\s*(https?://\S+)$', line)
        if match:
            metadata_str = match.group(1).strip()
            url = match.group(2).strip()
            metadata_fields = metadata_str.split("<SEP>")
            if len(metadata_fields) >= 4:
                # Assume that fields 3 and 4 (0-indexed: index 2 and 3) are artist and song title.
                artist = metadata_fields[2].strip()
                song_title = metadata_fields[3].strip()
            else:
                print(f"Warning: Insufficient metadata in line: {line}")
                artist, song_title = "Unknown Artist", "Unknown Title"
        else:
            print(f"Warning: Could not parse line: {line}")
            return

        # If a file with the exact filename already exists, skip the download.
        if is_duplicate(artist, song_title, DOWNLOADS_DIR):
            print(f"Skipping duplicate: {artist} - {song_title}")
            return

        print(f"Downloading: {artist} - {song_title}")
        subprocess.run([sys.executable, '-m', 'spotdl', url], check=True)

def download_urls_from_file(file_path):
    """
    Reads the given file (expected to be spotify_urls_merged.txt) line by line.
    Returns a list where each element is a non-empty line.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    # Use the merged Spotify URLs file instead of the clean one.
    #IMPORTANT: replace file_path value with your designated song list file!!!
    file_path = "spotify_urls_merged_1.txt"
    urls = download_urls_from_file(file_path)
    # Use a ThreadPoolExecutor to download concurrently.
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_url, urls)



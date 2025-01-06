import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading
from ratelimit import limits, sleep_and_retry  # You'll need to: pip install ratelimit

# Add these constants at the top
CALLS_PER_SECOND = 5  # Conservative rate limit
THIRTY_SECONDS = 30
MAX_RETRIES = 3

@sleep_and_retry
@limits(calls=CALLS_PER_SECOND * THIRTY_SECONDS, period=THIRTY_SECONDS)
def rate_limited_search(sp, search_query):
    return sp.search(q=search_query, type='track', limit=1)

def get_spotify_track_url(track_name):
    # Set up authentication with Spotify
    # You'll need to get these credentials from your Spotify Developer Dashboard
    client_id = '59b2e38f740645ae9fc2c86e066a0c75'
    client_secret = '7886b4b46f4d467a8df8816bead66122'
    
    # Initialize the Spotify client
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Search for the track
    results = sp.search(q=track_name, type='track', limit=1)
    
    # Check if we found any tracks
    if results['tracks']['items']:
        # Get the first track's external URL
        track_url = results['tracks']['items'][0]['external_urls']['spotify']
        return track_url
    else:
        return None

def process_track(sp, line):
    try:
        # Decode and split the line
        parts = line.split('<SEP>')
        if len(parts) != 4:
            return None
        
        # Use both artist and track name for more accurate search
        artist = parts[2]
        track_name = parts[3]
        search_query = f"{track_name} artist:{artist}"
        
        # Replace direct sp.search with rate-limited version
        for attempt in range(MAX_RETRIES):
            try:
                results = rate_limited_search(sp, search_query)
                break
            except Exception as e:
                if "429" in str(e) and attempt < MAX_RETRIES - 1:  # Rate limit error
                    wait_time = (2 ** attempt) * 1  # Exponential backoff
                    print(f"Rate limit hit, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                raise e
        
        if results['tracks']['items']:
            track_url = results['tracks']['items'][0]['external_urls']['spotify']
            print(f"Found URL for: {artist} - {track_name}")  # Add debug logging
            return (line, track_url)
        else:
            print(f"No match found for: {artist} - {track_name}")  # Add debug logging
        
        # Add a small delay to respect rate limits
        time.sleep(0.1)
        return None
        
    except Exception as e:
        print(f"Error processing track: {line}")
        print(f"Error details: {str(e)}")
        return None

def process_tracks_file(input_path, output_path):
    print(f"\nInitializing Spotify client...")
    # Initialize Spotify client
    client_id = '59b2e38f740645ae9fc2c86e066a0c75'
    client_secret = '7886b4b46f4d467a8df8816bead66122'
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    print("Spotify client initialized successfully!")

    print(f"\nProcessing tracks...")
    processed_count = 0
    failed_count = 0
    
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            try:
                parts = line.strip().split('<SEP>')
                if len(parts) != 4:
                    continue
                
                artist = parts[2]
                track_name = parts[3]
                search_query = f"{track_name} artist:{artist}"
                print(search_query)
                # Search for track
                results = sp.search(q=search_query, type='track', limit=1)
                print(results)
                if results['tracks']['items']:
                    track_url = results['tracks']['items'][0]['external_urls']['spotify']
                    outfile.write(f"{line.strip()}\t{track_url}\n")
                    processed_count += 1
                    print(f"Found URL for: {artist} - {track_name}")
                else:
                    failed_count += 1
                    print(f"No match found for: {artist} - {track_name}")
                
                # Add a small delay to respect rate limits
                time.sleep(0.1)
                
            except Exception as e:
                failed_count += 1
                print(f"Error processing track: {line.strip()}")
                print(f"Error details: {str(e)}")
    
    print(f"\nProcess completed!")
    print(f"Successfully processed: {processed_count} tracks")
    print(f"Failed to match: {failed_count} tracks")

if __name__ == "__main__":
    input_path = "missing_songs.txt"
    output_path = "spotify_urls_2.txt"
    process_tracks_file(input_path, output_path)

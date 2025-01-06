import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from concurrent.futures import ThreadPoolExecutor
import time

def setup_spotify():
    # You'll need to set these environment variables or pass them directly
    client_credentials_manager = SpotifyClientCredentials(client_id = '59b2e38f740645ae9fc2c86e066a0c75',
    client_secret = '7886b4b46f4d467a8df8816bead66122')
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_track_url(line, sp):
    try:
        # Split the line by separator and get track title
        parts = line.strip().split('<SEP>')
        if len(parts) < 4:
            return None
        
        track_title = parts[3]
        artist = parts[2]
        
        # Search for the track
        results = sp.search(q=f"track:{track_title} artist:{artist}", type='track', limit=1)    
        print(results)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            return {
                'title': track_title,
                'artist': artist,
                'url': track['external_urls']['spotify']
            }
        return None
    except Exception as e:
        print(f"Error processing {track_title}: {str(e)}")
        return None

def process_file(filename, max_workers=10):
    sp = setup_spotify()
    track_urls = []
    
    # Read all lines from the file
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Use ThreadPoolExecutor to process lines concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create futures for each line
        futures = [executor.submit(get_track_url, line, sp) for line in lines if '<SEP>' in line]
        print(futures)
        # Process completed futures
        for future in futures:
            result = future.result()
            if result:
                track_urls.append(result)
    
    return track_urls

def main():
    start_time = time.time()
    
    # Process the file
    results = process_file('tracks_per_year_sampled.txt')
    
    # Write results to file
    with open('spotify_urls.txt', 'w', encoding='utf-8') as f:
        for result in results:
            f.write(f"Track: {result['title']}\n")
            f.write(f"Artist: {result['artist']}\n")
            f.write(f"Spotify URL: {result['url']}\n")
            f.write("---\n")
    
    print(f"Processed {len(results)} tracks in {time.time() - start_time:.2f} seconds")
    print(f"Results written to spotify_urls.txt")

if __name__ == "__main__":
    main()
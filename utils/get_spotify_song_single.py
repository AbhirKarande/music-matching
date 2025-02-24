import sys
import subprocess

def download_url(url):
    if url.strip():
        subprocess.run([sys.executable, '-m', 'spotdl', url], check=True)

# Example usage
spotify_url = "https://open.spotify.com/track/41xkJRr0hLgQlxSm89e5s9"  # Replace with actual Spotify URL
download_url(spotify_url)
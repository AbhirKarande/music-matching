import subprocess
import os
import sys
import shutil

def get_spotdl_path():
    """Get the full path to spotdl executable in the virtual environment."""
    # Try common virtual environment binary locations
    possible_paths = [
        os.path.join(sys.prefix, 'bin', 'spotdl'),  # Unix-like systems
        os.path.join(sys.prefix, 'Scripts', 'spotdl.exe'),  # Windows
        os.path.join(sys.prefix, 'Scripts', 'spotdl'),  # Windows without extension
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
            
    return None

def check_spotdl_installation():
    """Check if spotdl is installed and accessible."""
    spotdl_path = get_spotdl_path()
    if not spotdl_path:
        print("Error: 'spotdl' command not found. Please install spotdl first.")
        print("You can install it using: pip install spotdl")
        print("\nIf already installed, try these troubleshooting steps:")
        print("1. Ensure you're in the correct virtual environment")
        print("2. Run: which spotdl")
        print("3. Try reinstalling: pip uninstall spotdl && pip install spotdl")
        sys.exit(1)
    return spotdl_path

def download_url(url, download_dir, spotdl_path):
    if url.strip():
        try:
            # Call spotdl with full path
            subprocess.run([spotdl_path, '-o', download_dir, url], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {url}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error downloading {url}: {str(e)}")

def download_all_urls(file_path, download_dir='downloads'):
    # Check for spotdl installation first
    spotdl_path = check_spotdl_installation()
    
    # Ensure the download directory exists
    os.makedirs(download_dir, exist_ok=True)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                url = line.strip()
                if url:  # skip blank lines
                    print(f"Downloading: {url}")
                    download_url(url, download_dir, spotdl_path)
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    spotify_urls_file = "spotify_urls_clean.txt"
    download_all_urls(spotify_urls_file) 
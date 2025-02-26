import os

def cleanup_spotify_urls():
    # List all mp3 files in the current directory (utils/downloads)
    mp3_files = [f for f in os.listdir(".") if f.lower().endswith(".mp3")]
    
    # Build a set of (artist, title) pairs from the mp3 filenames.
    # Expect filenames like "Artist - Title.mp3"
    existing_songs = set()
    for filename in mp3_files:
        base, _ = os.path.splitext(filename)
        if " - " in base:
            artist, title = base.split(" - ", 1)
            # using lower() to compare in a case-insensitive fashion
            existing_songs.add((artist.strip().lower(), title.strip().lower()))
        else:
            print(f"Skipping file with unexpected name format: {filename}")
    
    # Process each of the split Spotify files
    for i in range(1, 5):  # Process files 1 through 4
        spotify_file = f"spotify_urls_merged{i}.txt"
        
        if not os.path.exists(spotify_file):
            print(f"Warning: {spotify_file} not found, skipping.")
            continue
        
        # Read all lines from the spotify merged file
        with open(spotify_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        kept_lines = []
        removed_count = 0

        for line in lines:
            # Split the line on the <SEP> string.
            parts = line.rstrip("\n").split("<SEP>")
            # We expect at least 4 parts: year, some id, artist, and a field containing title and URL.
            if len(parts) < 4:
                # if the format is not as expected, we simply keep the line
                kept_lines.append(line)
                continue
            
            artist = parts[2].strip()
            title_field = parts[3].strip()
            # In many cases the title field also contains the URL separated by a tab.
            if "\t" in title_field:
                title = title_field.split("\t")[0].strip()
            else:
                title = title_field

            # If this (artist, title) is found within our MP3 files, skip the line (i.e. delete it)
            if (artist.lower(), title.lower()) in existing_songs:
                removed_count += 1
                continue
            
            # Otherwise, keep the line.
            kept_lines.append(line)
        
        # Rewrite the spotify file with the non-matching lines.
        with open(spotify_file, "w", encoding="utf-8") as f:
            f.writelines(kept_lines)
        
        print(f"Removed {removed_count} matching lines from {spotify_file}")

if __name__ == "__main__":
    cleanup_spotify_urls()

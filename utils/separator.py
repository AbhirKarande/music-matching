def parse_file(filename):
    songs = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                parts = line.strip().split('<SEP>')
                if len(parts) >= 3:
                    # Use year, id, and artist+title as key
                    key = f"{parts[0]}<SEP>{parts[1]}<SEP>{parts[2]}"
                    songs[key] = line.strip()
    return songs

# Parse both files
spotify_songs = parse_file('spotify_urls.txt')
sampled_songs = parse_file('tracks_per_year_sampled.txt')

# Find songs in sampled that aren't in spotify
missing_songs = []
for key, line in sampled_songs.items():
    if key not in spotify_songs:
        missing_songs.append(line)

# Write missing songs to new file
with open('missing_songs.txt', 'w', encoding='utf-8') as f:
    for song in missing_songs:
        f.write(f"{song}\n")

print(f"Found {len(missing_songs)} songs without Spotify URLs")

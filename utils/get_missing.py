# Read Spotify URLs file and extract song identifiers (before the tab)
with open('spotify_urls_2.txt', 'r') as f:
    spotify_songs = {line.split('\t')[0].strip() for line in f}

# Compare with missing songs and write remaining entries
with open('missing_songs.txt', 'r') as f_in, \
     open('remaining_songs.txt', 'w') as f_out:
    
    for line in f_in:
        stripped_line = line.strip()
        # Check if this exact song entry exists in Spotify URLs (without URL)
        if stripped_line not in spotify_songs:
            f_out.write(line)

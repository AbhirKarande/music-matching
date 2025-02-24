def merge_spotify_files():
    # Files to merge
    files = [
        'spotify_urls_so_far.txt',
        'spotify_urls_2.txt',
        'spotify_urls_3.txt'
    ]
    
    # Set to store unique lines
    unique_lines = set()
    
    # Read each file and add lines to set
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Strip whitespace and add to set
                unique_lines.add(line.strip())
    
    # Write unique lines to new file
    with open('spotify_urls_merged.txt', 'w', encoding='utf-8') as f:
        for line in sorted(unique_lines):
            f.write(line + '\n')

if __name__ == "__main__":
    merge_spotify_files()

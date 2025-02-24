import re

with open('spotify_urls_merged.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    
# Extract just the Spotify URLs using regex
urls = re.findall(r'https://open\.spotify\.com/track/[a-zA-Z0-9]+', content)

# Write unique URLs to file
with open('spotify_urls_clean.txt', 'w', encoding='utf-8') as file:
    for url in set(urls):  # set() removes duplicates
        file.write(url + '\n')

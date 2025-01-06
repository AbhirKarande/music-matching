import random
from collections import defaultdict

def stratified_sample_tracks(target_sample_size=150000):
    # Read all lines from the file
    import requests
    url = "http://millionsongdataset.com/sites/default/files/AdditionalFiles/tracks_per_year.txt"
    response = requests.get(url)
    lines = response.text.splitlines()
    
    # Group tracks by year
    tracks_by_year = defaultdict(list)
    for line in lines:
        try:
            year = int(line.split('<SEP>')[0])
            tracks_by_year[year].append(line)
        except (ValueError, IndexError):
            continue
    
    # Perform stratified sampling
    sampled_tracks = []
    years = sorted(tracks_by_year.keys())
    samples_per_year = target_sample_size // len(years)
    
    for year in years:
        year_tracks = tracks_by_year[year]
        # Take either samples_per_year or all tracks if less are available
        sample_size = min(samples_per_year, len(year_tracks))
        sampled_tracks.extend(random.sample(year_tracks, sample_size))
    
    # Shuffle the final sample
    random.shuffle(sampled_tracks)
    
    # Write the sampled tracks back to the file
    with open('tracks_per_year_sampled.txt', 'w', encoding='utf-8') as file:
        for track in sampled_tracks:
            file.write(f"{track}\n")

if __name__ == '__main__':
    stratified_sample_tracks()

import subprocess
from concurrent.futures import ThreadPoolExecutor

def download_url(url):
  if url.strip():
    subprocess.run(['spotdl', url], check = True)


urls = []
with open('spotify_urls_clean.txt', 'r') as f:
   urls = f.read().split('\n')

with ThreadPoolExecutor(max_workers = 5) as executor:
     executor.map(download_url, urls)


#23246

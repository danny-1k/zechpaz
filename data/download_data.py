from urllib.request import urlopen
from bs4 import BeautifulSoup
from utils import download_from_url, unzip_file
import os

from tqdm import tqdm

num = 362

base_url = 'https://www.pgnmentor.com/'
url = base_url + 'files.html'
page = urlopen(url).read()
soup = BeautifulSoup(page, 'html.parser')

download_links = list(map((lambda x: x['href']), soup.find_all(
    'a', {'class': 'view'}, string='Download')))

print('Downloading PGN files')

for i in tqdm(range(num)):
    url = base_url+download_links[i]

    if url.rsplit('/', 1)[1] not in os.listdir('data/raw'):

        download_from_url(url, 'data/raw')
    else:
        print(f'Already downloaded {url.rsplit("/", 1)[1]}')
print('Unzipping PGN files')
for f in tqdm(os.listdir('data/raw')):
    if '.zip' in f:
        unzip_file('data/raw/'+f, 'data/raw', remove=True)

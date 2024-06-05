import os 
import requests
from bs4 import BeautifulSoup

def fetch_image_urls(restaurant_url):
    response = requests.get(restaurant_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_urls = [img['src'] for img in soup.find_all('img') if 'menu' in img['src']]
    return image_urls

def download_images(image_urls, save_dir='data/images'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for i, url in enumerate(image_urls):
        response = requests.get(url)
        with open(f'{save_dir}/{i}.jpg', 'wb') as f:
            f.write(response.content)
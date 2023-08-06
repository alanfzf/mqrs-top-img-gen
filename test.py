from util import scraper
from dotenv import load_dotenv

load_dotenv()

users = ['alanfvn', 'themqrs', 'juanKamanei321']
imgs = scraper.download_user_images(users)

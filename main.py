from util import excel 
from util import format
from util import scraper
from util import img
from dotenv import load_dotenv

# Load env
load_dotenv()

# Excel stuff
table = excel.get_data_from_table()
scores = excel.get_scores_from_table(table)
users = excel.get_values_from_col(table, 1)

# Validate data
valid_users = format.validate_users(users)

# Scrape profile pictures
imgs = scraper.download_user_images(valid_users)

# Generate the images
score = img.ScoreGenerator(scores, imgs)
score.generate_images()
score.generate_names()

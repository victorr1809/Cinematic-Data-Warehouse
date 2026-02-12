import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_KEY = os.getenv("API_KEY")
OUTPUT_FILE = "/Users/manh/Documents/GitHub/IMDB-Movie-DWH/crawled_data"


MEDIA_TYPE = 'movie'
START_DATE = ''
END_DATE = ''

# MEDIA_MOVIE_TYPE = "movie"  
# MEDIA_TVSHOW_TYPE = 'tvShow'
# START_YEAR = 2023
# END_YEAR = 2024
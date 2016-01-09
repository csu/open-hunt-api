from datetime import datetime

from bs4 import BeautifulSoup
import requests

OPENHUNT_BASE_URL = 'https://www.openhunt.co/date/'

def get_listings_for_date(date=None):
  # if no date specified, use today
  if not date:
    date = datetime.today().strftime("%Y%m%d")
  
  url = OPENHUNT_BASE_URL + date
  soup = BeautifulSoup(requests.get(url).content, 'html.parser')
  
  items = soup.findAll('div', {'class': ['project-listing', 'item', 'row']})
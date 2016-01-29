from datetime import datetime

from bs4 import BeautifulSoup
from pytz import timezone
import requests

OPENHUNT_BASE_URL = 'https://www.openhunt.co/date/'

def get_listings_for_date(date=None):
  # if no date specified, use today
  if not date:
    date = datetime.now(tz=timezone('US/Pacific')).strftime("%Y%m%d")
  else:
    # validate date
    try:
      datetime.strptime(date, "%Y%m%d")
    except:
      return {'error': 'Date formatted incorrectly.'}

  return date
  
  url = OPENHUNT_BASE_URL + date
  soup = BeautifulSoup(requests.get(url).content, 'html.parser')
  
  items = soup.findAll('div', {'class': ['project-listing', 'item', 'row']})

  results = []
  titles = []

  for item in items:
    title_elem = item.find('a', {'class': 'title'})
    if not title_elem:
      continue

    title_text = title_elem.text.replace('\n', '')

    if title_text in titles:
      continue
    titles.append(title_text)

    item_dict = {}

    try:
      item_dict['title'] = title_text
    except:
      item_dict['title'] = 'API error'

    try:
      item_dict['href'] = title_elem['href']
    except:
      item_dict['href'] = 'API error'

    try:
      item_dict['description'] = item.find('div', {'class': 'description'}).text.replace('\n', '')
    except:
      item_dict['description'] = 'API error'

    try:
      item_dict['score'] = int(item.find('div', {'class': 'counter'}).text)
    except:
      item_dict['score'] = 'API error'

    try:
      item_dict['author'] = item.find('a', {'class': 'user-avatar'})['href'][2:]
    except:
      item_dict['author'] = 'API error'
    
    results.append(item_dict)

  return results
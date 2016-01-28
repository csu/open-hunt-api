from datetime import datetime

from bs4 import BeautifulSoup
import requests

OPENHUNT_BASE_URL = 'https://www.openhunt.co/date/'

def get_listings_for_date(date=None):
  # if no date specified, use today
  if not date:
    date = datetime.today().strftime("%Y%m%d")
  else:
    # validate date
    try:
      datetime.strptime(date, "%Y%m%d")
    except:
      return {'error': 'Date formatted incorrectly.'}
  
  url = OPENHUNT_BASE_URL + date
  soup = BeautifulSoup(requests.get(url).content, 'html.parser')
  
  items = soup.findAll('div', {'class': ['project-listing', 'item', 'row']})

  results = []

  for item in items:
    title_elem = item.find('a', {'class': 'title'})

    item_dict = {}

    try:
      item_dict['title'] = title_elem.text.replace('\n', '')
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
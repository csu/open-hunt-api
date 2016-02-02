import argparse
import os

from feedgen.feed import FeedGenerator
from flask import Flask, jsonify
from flask.ext.cache import Cache

import pyopenhunt

app = Flask(__name__)

# could use memcached or something, but probably overkill
# just going to use any caching to limit # of requests to open hunt
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

BASE_URL = 'http://openhunt.christopher.su'

@app.route('/')
@cache.cached(timeout=600)
def index():
  return jsonify({
    'author': {
      'name': 'Christopher Su',
      'url': 'http://christopher.su',
    },
    'project': {
      'name': 'Open Hunt API',
      'url': 'https://github.com/csu/open-hunt-api',
    },
    'base_url': BASE_URL,
    'endpoints': {
      'today_url': '%s/today' % BASE_URL,
      'today_rss_url': '%s/today/rss' % BASE_URL,
      'today_atom_url': '%s/today/atom' % BASE_URL,
      'date_url': '%s/{date_YYYYMMDD}' % BASE_URL,
      'date_rss_url': '%s/{date_YYYYMMDD}/rss' % BASE_URL,
      'date_atom_url': '%s/{date_YYYYMMDD}/atom' % BASE_URL,
    }
  })

@app.route('/<date_string>')
@cache.cached(timeout=300)
def specific_date(date_string):
  if date_string == 'today':
    return jsonify({
      'items': pyopenhunt.get_listings_for_date()
    })

  return jsonify({
    'items': pyopenhunt.get_listings_for_date(date_string)
  })

def gen_rss(items, date_string, atom=False):
  fg = FeedGenerator()
  fg.title('Open Hunt: %s' % date_string)
  fg.id('%s/%s' % (BASE_URL, date_string))

  # setting more fields that we don't really need
  # to appease the atom/rss generators
  fg.author({'name': 'Christopher Su', 'email': 'oh-api@christopher.su'})
  fg.description('Open Hunt items for %s' % date_string)
  fg.subtitle('Open Hunt items for %s' % date_string)
  fg.language('en')

  if atom:
    fg.link({'href': '%s/%s/atom' % (BASE_URL, date_string), 'rel': 'self'})
  else:
    fg.link({'href': '%s/%s/rss' % (BASE_URL, date_string), 'rel': 'self'})

  counter = 0
  for item in items:
    fe = fg.add_entry()

    # id is a mandatory field for atom
    # we're using it wrong here, but oh well
    # should probably use open hunt's slugs instead
    if atom:
      fe.id(counter)
      counter += 1

    fe.link({'href': item['href'], 'rel': 'alternate'})
    fe.title(item['title'])
    fe.description(str(item['score']))
    fe.content(item['description'])
    fe.author({'name': item['author'], 'email': '@%s' % item['author']})

  if atom:
    return fg.atom_str(pretty=True)
  return fg.rss_str(pretty=True)

@app.route('/<date_string>/rss')
@cache.cached(timeout=300)
def specific_date_rss(date_string):
  if date_string == 'today':
    return gen_rss(pyopenhunt.get_listings_for_date(), date_string)
  return gen_rss(pyopenhunt.get_listings_for_date(date_string), date_string)

@app.route('/<date_string>/atom')
@cache.cached(timeout=300)
def specific_date_atom(date_string):
  if date_string == 'today':
    return gen_rss(pyopenhunt.get_listings_for_date(),
                    date_string, atom=True)
  return gen_rss(pyopenhunt.get_listings_for_date(date_string),
            date_string, atom=True)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
  args = parser.parse_args()

  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=args.debug)
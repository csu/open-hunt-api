import argparse
import os

from flask import Flask, jsonify
from flask.ext.cache import Cache

import pyopenhunt

app = Flask(__name__)

# could use memcached or something, but probably overkill
# just going to use any caching to limit # of requests to open hunt
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

@app.route('/')
@cache.cached(timeout=180)
def index():
  return jsonify({
    'author': {
      'name': 'Christopher Su',
      'url': 'http://christopher.su'
    },
    'project': {
      'name': 'Open Hunt API',
      'url': 'https://github.com/csu/open-hunt-api'
    },
    'base_url': 'http://openhunt.christopher.su',
    'endpoints': {
      'today_url': 'http://openhunt.christopher.su/today',
      'date_url': 'http://openhunt.christopher.su/{date_YYYYMMDD}'
    }
  })

@app.route('/<date_string>')
@cache.cached(timeout=180)
def specific_date(date_string):
  if date_string == 'today':
    return jsonify({
      'items': pyopenhunt.get_listings_for_date()
    })

  return jsonify({
    'items': pyopenhunt.get_listings_for_date(date_string)
  })

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
  args = parser.parse_args()

  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=args.debug)
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
      'items': pyopenhunt.get_listings_for_date()
    })

@app.route('/<date_string>')
@cache.cached(timeout=180)
def specific_date(date_string):
    return jsonify({
      'items': pyopenhunt.get_listings_for_date(date_string)
    })

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
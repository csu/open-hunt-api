# Open Hunt API
An unofficial, read-only API for Open Hunt.

## Endpoints
* `GET /`: Get API information
* `GET /today`: Get items for today
* `GET /<date in YYYYMMDD format>`: Get items for specific date
* `GET /today/rss`: Get items for today as a RSS feed
* `GET /<date in YYYYMMDD format>/rss`: Get items for specific date as a RSS feed
* `GET /today/atom`: Get items for today as an Atom feed
* `GET /<date in YYYYMMDD format>/atom`: Get items for specific date as an Atom feed

## Result Format
```
{
  "items": [
    {
      "author": "maddynator", 
      "description": "Creating, Tracking and Analyzing workouts has never been this simple.", 
      "href": "https://...", 
      "score": 10, 
      "title": "GYMINUTES"
    }, 
    {
      "author": "ronnhere", 
      "description": "Take bookmarking to next level with power of Notes, Labels and read later", 
      "href": "https://...", 
      "score": 8, 
      "title": "Basket for Chrome"
    }, 
    {
      "author": "AnnoyingStuffCo", 
      "description": "Quirky Unicorn Card with a Glittery Surprise", 
      "href": "http://...", 
      "score": 3, 
      "title": "Unicorn Surprise"
    }, 
    {
      "author": "Festspec", 
      "description": "Hotel bookings near festivals and special events", 
      "href": "http://...", 
      "score": 2, 
      "title": "FestivalSpecials"
    }
  ]
}
```
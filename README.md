# Event scraper
Scrape events from websites and add them to a Google Calendar.

## Usage
1. Clone this repository.
2. Get a Google Calendar API [key](https://console.developers.google.com/flows/enableapi?apiid=calendar).
3. Store the client secret in `~/.credentials` as `client_secret.json`
4. Update the variable `X_CALENDAR_ID` in `main.py` to point to your own calendar.
5. Run `python3 main.py`

## Requirements

```
bs4
dateutil
google-api-python-client
```

## Current Calendars
Currently this repository supports scraping the following websites for events:

- [CREA](crea.nl): the cultural student center of the University of Amsterdam ([calendar](https://calendar.google.com/calendar/embed?src=1if765nauiejb3goqgdij4jk1k%40group.calendar.google.com&ctz=Europe/Amsterdam))

"""
Scrape events from the CREA cultural center calendar of the University of
Amsterdam and format them for use in Google Calendar.
"""

import datetime
from dateutil.relativedelta import relativedelta
import requests
from bs4 import BeautifulSoup as beautifulsoup
import hashlib

CREA_AGENDA_ADDRESS = "http://www.crea.uva.nl/agenda.php?jaar={0}&maand={1}"
CREA_MORE_INFO_ADDRESS = "http://www.crea.uva.nl/{0}"
CREA_LOCATION = "Nieuwe Achtergracht 170, Amsterdam"


def get_months():
    """Get the current and next two months as a number (year-month)."""
    class Month:
        def __init__(self, date):
            self.month = str(date.month).rjust(2, "0")
            self.year = str(date.year)
    today = datetime.date.today()
    this_month = Month(today)
    next_month = Month(today + relativedelta(months=1))
    month_after_next = Month(today + relativedelta(months=2))

    return this_month, next_month, month_after_next


def get_content():
    """Get content of the calendar webpage for the current and next two month."""
    months = get_months()
    content = []
    for month in months:
        calendar_address = CREA_AGENDA_ADDRESS.format(month.year, month.month)
        calendar_page = requests.get(calendar_address)
        content.append({"content": calendar_page.text, "month": month})
    return content


def get_events():
    """Get the events from the webpage and format them for use in Google Calendar."""
    content = get_content()
    events = []
    for page in content:
        month = page["month"].month
        year = page["month"].year
        soup = beautifulsoup(page["content"], "lxml")
        agenda_items = soup.find_all('ul', class_='agendaitems', attrs={})

        # The calendar page has two columns for events.
        for column in agenda_items:
            items = column.find_all('li')  # Each event is a list.
            for item in items:
                title = item.find("span", class_='kopje').get_text()
                url = CREA_MORE_INFO_ADDRESS.format(item.find_all("a", href=True)[0]['href'])
                description = item.find('span', class_='tekst').get_text()
                item_datetime = item.find('em', class_="datum").get_text().split('|')

                dates = ['-'.join([year, month, a[1]]) for a in [d.strip().split(' ') for d in item_datetime[:-1]]]


                # Gracefully handle events that occur on multiple days.
                for date in dates:
                    start_time = item_datetime[-1].strip() + ':00'
                    event_start = date + 'T' + start_time
                    event_end = (datetime.datetime.strptime(event_start, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S')

                    # Hashes are used as a unique identifier to prevent the same event from being added twice.
                    event_hash = hashlib.sha224(str(title + url + date + start_time + description).encode('utf-8')).hexdigest()

                    event = {"summary": title,
                             "start": {
                                    "dateTime": event_start,
                                    "timeZone": "Europe/Amsterdam"
                                },
                             "end": {
                                    "dateTime": event_end,
                                    "timeZone": "Europe/Amsterdam"
                                },
                             "description": url + description,
                             "id": event_hash}
                    events.append(event)
    return events

if __name__ == '__main__':
    print(get_events())

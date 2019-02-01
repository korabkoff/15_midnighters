import requests
from pytz import timezone
from datetime import datetime


def load_attempts(url):
    page = 1
    while True:
        page += 1
        response = requests.get(url, params={'page': page})
        if response.status_code != 200:
            break
        yield from response.json()['records']


def get_midnighters(record_generator):
    owls = []
    for record in record_generator:

        utc_timestamp = record['timestamp']
        the_timezone = timezone(record['timezone'])
        username = record['username']

        local_date_time = datetime.fromtimestamp(utc_timestamp, tz=the_timezone)

        start_hours_idx = 11
        end_hours_idx = 13
        hours = int(str(local_date_time)[start_hours_idx:end_hours_idx])

        last_night_hour = 6
        if hours < last_night_hour and username not in owls:
            owls.append(username)
            yield username


if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/'

    for midnighter in get_midnighters(load_attempts(url)):
        print(midnighter)

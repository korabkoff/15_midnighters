import requests
import pytz
from datetime import datetime


def load_attempts(url):
    first_page_number = 1
    pages = requests.get(url, params={'page': first_page_number}).json()['number_of_pages']
    for page in range(pages):
        yield requests.get(url, params={'page': page+1}).json()['records']


def get_midnighters(records_generator):
    owls = []
    for record in records_generator:
        for idx in range(len(record)):
            utc_timestamp = record[idx]['timestamp']
            the_timezone = pytz.timezone(record[idx]['timezone'])
            username = record[idx]['username']
            utc_date_time = pytz.utc.localize(datetime.utcfromtimestamp(utc_timestamp))
            local_date_time = utc_date_time.astimezone(the_timezone)
            start_hours_idx = 11
            end_hours_idx = 13
            hours = str(local_date_time)[start_hours_idx:end_hours_idx]
            last_night_hour = 6
            if int(hours) < last_night_hour and username not in owls:
                owls.append(username)
    return owls

if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/'

    for midnighter in get_midnighters(load_attempts(url)):
        print(midnighter)

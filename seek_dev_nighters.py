import requests
import pytz
from datetime import datetime


def load_attempts(url):
    first_page = str(1)
    pages = requests.get(url+first_page).json()['number_of_pages']
    for page in range(pages):
        yield requests.get('{}{}'.format(url, str(page+1))).json()['records']


def get_midnighters(records_generator):
    owls = []
    for record in records_generator:
        for idx in range(len(record)):
            utc_timestamp = record[idx]['timestamp']
            the_timezone = pytz.timezone(record[idx]['timezone'])
            username = record[idx]['username']
            utc_date_time = pytz.utc.localize(datetime.utcfromtimestamp(utc_timestamp))
            local_date_time = utc_date_time.astimezone(the_timezone)
            hours = str(local_date_time)[11:13]
            last_night_hour = 6
            if int(hours) < last_night_hour and username not in owls:
                owls.append(username)
    return owls

if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/?page='

    for name in get_midnighters(load_attempts(url)):
        print(name)

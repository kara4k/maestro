# coding=utf-8

import json

import bs4
import requests

from track import Track

ENDPOINT = 'http://zaycev.net/search.html?'
URL_START = 'http://zaycev.net'

page = 1
last_query = ''


def show_tracks(query):
    global page, last_query
    page = 1
    last_query = query

    print 'Searching...'
    return get_tracks(create_url(query, '1'))


def show_more():
    global page
    page += 1

    print 'Searching more...'
    return get_tracks(create_url(last_query, str(page)))


def create_url(query, page):
    params = {'query_search': query, 'page': page}
    ready_params = ['='.join(item) for item in params.iteritems()]
    return '%s%s' % (ENDPOINT, '&'.join(ready_params))


def get_tracks(url):
    response = requests.get(url)
    response.raise_for_status()

    elements = bs4.BeautifulSoup(response.content, 'lxml').select('div[data-url^="/musicset/play/"]')
    tracks_list = []

    for element in elements:
        children = element.findChildren('a', recursive=True)

        if len(children) < 3:
            continue

        artist = children.__getitem__(0).getText()
        name = children.__getitem__(1).getText()
        json = '%s%s' % (URL_START, element.get('data-url'))
        duration = element.findChildren('div', {'class': 'musicset-track__duration'}, recursive=True) \
            .__getitem__(0).getText()
        path = get_track_path(json)

        tracks_list.append(Track(artist, name, json, duration, path))

    return tracks_list


def get_track_path(json_path):
    json_content = requests.get(json_path, 'lxml').content
    loads = json.loads(json_content)
    return loads['url'].split('?')[0]


if __name__ == '__main__':
    tracks = get_tracks(create_url('deftones', '1'))

    for track in tracks:
        print track

    print '\nTotal: %d' % len(tracks)

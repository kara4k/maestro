import os
import sys
from datetime import datetime

import pyperclip

reload(sys)
sys.setdefaultencoding('utf8')

ACTION_SEARCH = 0
ACTION_DOWNLOAD = 1
ACTION_MORE = 2
ACTION_APPEND = 3
ACTION_PLAY = 4
ACTION_PAUSE = 5
ACTION_STOP = 6
ACTION_LIST = 7
ACTION_QUIT = 8
ACTION_NEXT = 9
ACTION_FILTER = 10
ACTION_INFO = 11
ACTION_COPY = 12
ACTION_WRITE = 13

SEARCH = ['s', '-s', '--search']
DOWNLOAD = ['d', '-d', '--download']
MORE = ['m', '-m', '--more']
APPEND = ['a', '-a', '--append']
PLAY = ['p', '-p', '--play']
PAUSE = ['ps', '-ps', '--pause']
STOP = ['st', '-st', '--stop']
LIST = ['l', '-l', '--list']
QUIT = ['q', '-q', '--quit']
NEXT = ['n', '-n', '--next']
FILTER = ['f', '-f', '--filter']
INFO = ['i', '-i', '--info']
COPY = ['c', '-c', '--copy']
WRITE = ['w', '-w', '--write']

ACTIONS = [SEARCH, DOWNLOAD, MORE, APPEND, PLAY, PAUSE, STOP, LIST, QUIT, NEXT, FILTER, INFO, COPY, WRITE]


def get_action(line):
    params = line.split(' ')
    act = None

    if len(params) > 0:
        for action in ACTIONS:
            for c in action:
                if c.__eq__(params[0]):
                    act = ACTIONS.index(action)
                    break
    return act


def get_indexes(line):
    try:
        params = line.split(' ')
        track_indexes = []

        if len(params) > 1:
            indexes = params[1]
            indexes_split = indexes.split(',')

            for part in indexes_split:
                index_range = part.strip().split('-')

                if len(index_range) == 1:
                    track_indexes.append(int(index_range[0]))
                else:
                    start = int(index_range[0])
                    end = int(index_range[1])

                    while not start > end:
                        track_indexes.append(start)
                        start += 1

        return list(set(track_indexes))
    except ValueError:
        print 'Wrong indexes :('
        return []


def get_query(line):
    params = line.split(' ')

    if len(params) > 1:
        return ' '.join(params[1:])

    return None


def get_specified_path(line):
    params = line.split(' ')

    if len(params) > 2:
        return '%s%s' % ((os.path.dirname(params[2])), '/')
    return None


def get_addition_param(line):
    params = line.split(' ')

    if len(params) > 2:
        return params[2]
    return None


def filter_tracks(tracks, line):
    params = line.split(' ')
    filtered = []

    if len(params) > 1:

        for track in tracks:
            is_match = True

            for param in params[1:]:
                if not param.lower() in str(track).lower():
                    is_match = False

            if is_match:
                filtered.append(track)

        return filtered


def format_info(tracks):
    output = ''
    for track in tracks:
        output += '%s\n%s\n\n' % (track.__str__(), track.path)
    return output


def copy_info(tracks):
    info = format_info(tracks)
    pyperclip.copy(info.encode('utf-8'))
    print 'Info about %d tracks copied to clipboard' % len(tracks)


def get_current_time_str():
    return datetime.now().strftime("%d.%m.%Y_%H:%M:%S")


def write_info(tracks, filepath=None):
    if filepath is None:
        filepath = '%s/%s.tracks.txt' % (os.getcwd(), get_current_time_str())

    folder = os.path.dirname(filepath)
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(filepath, 'w+') as output_file:
        output_file.write(format_info(tracks))

    print 'Info about %d tracks written to file:\n%s' % (len(tracks), filepath)


if __name__ == '__main__':
    print get_indexes('m 1-4,7-12,9,9,9,123')
    print get_specified_path('d 3 /home/user/Music/')
    print get_current_time_str()

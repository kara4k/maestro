#!/usr/bin/env python
# coding=utf-8

import sys


from maestro_modules import actions, parser, dm
from maestro_modules.player import mpd_player

player = mpd_player.MpdPlayer()

tracks = []
filtered = []
is_filtering_mode = False


def do_action(line):
    global tracks, filtered, is_filtering_mode
    action = actions.get_action(line)

    if action is None:
        print_wrong_args()
    elif action == actions.ACTION_SEARCH:
        is_filtering_mode = False
        tracks = search_tracks(actions.get_query(line))
        show_tracks(tracks)
    elif action == actions.ACTION_LIST:
        is_filtering_mode = False
        show_tracks(tracks)
    elif action == actions.ACTION_INFO:
        print actions.format_info(get_selected_tracks(line))
    elif action == actions.ACTION_FILTER:
        is_filtering_mode = True
        if len(line.split(' ')) == 1:
            show_tracks(get_tracks_list())
        else:
            filtered = actions.filter_tracks(tracks, line)
            show_tracks(filtered)
    elif action == actions.ACTION_COPY:
        actions.copy_info(get_selected_tracks(line))
    elif action == actions.ACTION_WRITE:
        path = actions.get_addition_param(line)
        if path is None:
            actions.write_info(get_selected_tracks(line))
        else:
            actions.write_info(get_selected_tracks(line), path)
    elif action == actions.ACTION_MORE:
        load_more()
    elif action == actions.ACTION_DOWNLOAD:
        download(line)
    elif action == actions.ACTION_PLAY:
        play(line)
    elif action == actions.ACTION_NEXT:
        player.play_next()
    elif action == actions.ACTION_STOP:
        player.stop()
    elif action == actions.ACTION_APPEND:
        append(line)
    elif action == actions.ACTION_QUIT:
        exit()

    ask_for_action()


def print_wrong_args():
    print 'Wrong arguments :('


def get_tracks_list():
    if is_filtering_mode:
        return filtered
    return tracks


def load_more():
    more = parser.show_more()
    tracks.extend(more)
    show_tracks(get_tracks_list())


def exit():
    print 'Exit'
    sys.exit(-1)


def append(line):
    selected = get_selected_tracks(line)
    player.append_list(selected)


def get_selected_tracks(line):
    indexes = actions.get_indexes(line)
    selected = extract_selected(indexes, get_tracks_list())
    return selected


def play(line):
    indexes = actions.get_indexes(line)

    if len(indexes) == 0:
        player.play()
    else:
        selected = extract_selected(indexes, get_tracks_list())
        if len(selected) is not 0:
            player.play_tracks(selected)


def download(line):
    selected = get_selected_tracks(line)
    path = actions.get_specified_path(line)

    if path is None:
        dm.download(selected)
    else:
        dm.download(selected, path)


def extract_selected(indexes, tracks_list):
    list = []

    try:
        for index in indexes:
            list.append(tracks_list[index - 1])
    except IndexError:
        print_wrong_args()

    return list


def ask_for_action():
    do_action(raw_input('\nAction: '))


def search_tracks(query):
    if query is None:
        return []
    tracks = parser.show_tracks(query)
    return tracks


def show_tracks(track_list):
    if len(track_list) == 0:
        print 'Nothing found :('
    else:
        for track in track_list:
            print '[%d] %s' % (track_list.index(track) + 1, track.__str__())


if len(sys.argv) > 1:
    do_action('s %s' % ' '.join(sys.argv[1:]))
else:
    ask_for_action()

import os
import threading

import requests

threads = []


def download(tracks, dir=os.path.expanduser('~/Music/')):
    global threads
    threads = []
    print 'Downloading %d tracks' % len(tracks)

    for track in tracks:
        thread = threading.Thread(target=download_track, args=[track, dir])
        thread.start()
        threads.append(thread)

    wait_for_download()


def wait_for_download():
    for thread in threads:
        thread.join()


def download_track(track, dir):
    response = requests.get(track.path)

    if not os.path.exists(dir):
        os.makedirs(dir)

    filename = '%s%s - %s [%s].mp3' % (dir, track.artist, track.name, track.duration)

    with open(filename, 'wb+') as mp3_file:
        for chunk in response.iter_content(1000000):
            mp3_file.write(chunk)

    print 'Done %s' % filename

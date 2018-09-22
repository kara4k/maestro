import subprocess


def is_moc_running():
    result = subprocess.Popen(['pidof', 'mocp'], stdout=subprocess.PIPE)
    result.wait()
    return not result.stdout.readline().__eq__('')


def turn_on_moc_server():
    if not is_moc_running():
        print 'MOC server down, turning on...'
        subprocess.Popen(['mocp', '-S']).wait()


def play_tracks(tracks):
    turn_on_moc_server()

    print 'Clearing playlist...'
    subprocess.Popen(['mocp', '-c']).wait()

    append_list(tracks)
    play()


def append_list(tracks):
    print 'Adding %d tracks to playlist...' % len(tracks)
    for track in tracks:
        subprocess.Popen(['mocp', '-a', track.path]).wait()


def stop():
    subprocess.Popen(['mocp', '-s']).wait()


def play():
    print 'Playing'
    subprocess.Popen(['mocp', '-p']).wait()


def play_next():
    subprocess.Popen(['mocp', '-f'])


if __name__ == '__main__':
    turn_on_moc_server()
    play()

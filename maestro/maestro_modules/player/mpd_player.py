import subprocess

from player import Player


class MpdPlayer(Player):

    def is_player_running(self):
        result = subprocess.Popen(['pidof', 'mpd'], stdout=subprocess.PIPE)
        result.wait()
        return not result.stdout.readline().__eq__('')

    def turn_on_server(self):
        if not self.is_player_running():
            print 'MPD server down, turning on...'
            subprocess.Popen('mpd').wait()

    def play_tracks(self, tracks):
        self.turn_on_server()

        print 'Clearing playlist...'
        subprocess.Popen(['mpc', 'clear']).wait()

        self.append_list(tracks)
        self.play()

    def append_list(self, tracks):
        print 'Adding %d tracks to playlist...' % len(tracks)
        for track in tracks:
            subprocess.Popen(['mpc', 'add', track.path]).wait()

    def stop(self):
        subprocess.Popen(['mpc', 'stop']).wait()

    def play(self):
        subprocess.Popen(['mpc', 'play']).wait()

    def play_next(self):
        subprocess.Popen(['mpc', 'next'])
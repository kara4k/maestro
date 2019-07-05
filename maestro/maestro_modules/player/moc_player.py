import subprocess
from player import Player


class MocPlayer(Player):

    def is_player_running(self):
        result = subprocess.Popen(['pidof', 'mocp'], stdout=subprocess.PIPE)
        result.wait()
        return not result.stdout.readline().__eq__('')

    def turn_on_server(self):
        if not self.is_player_running():
            print 'MOC server down, turning on...'
            subprocess.Popen(['mocp', '-S']).wait()

    def play_tracks(self, tracks):
        self.turn_on_server()

        print 'Clearing playlist...'
        subprocess.Popen(['mocp', '-c']).wait()

        self.append_list(tracks)
        self.play()

    def append_list(self, tracks):
        print 'Adding %d tracks to playlist...' % len(tracks)
        for track in tracks:
            subprocess.Popen(['mocp', '-a', track.path]).wait()

    def stop(self):
        subprocess.Popen(['mocp', '-s']).wait()

    def play(self):
        print 'Playing'
        subprocess.Popen(['mocp', '-p']).wait()

    def play_next(self):
        subprocess.Popen(['mocp', '-f'])



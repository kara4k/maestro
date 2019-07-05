import abc


class Player:
    def __init__(self):
        pass

    @abc.abstractmethod
    def is_player_running(self):
        pass

    @abc.abstractmethod
    def turn_on_server(self):
        pass

    @abc.abstractmethod
    def play_tracks(self, tracks):
        pass

    @abc.abstractmethod
    def append_list(self, tracks):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def play(self):
        pass

    @abc.abstractmethod
    def play_next(self):
        pass




class TournamentStorage(object):
    def update_player(self, p):
        raise NotImplementedError
    def update_game(self, g):
        raise NotImplementedError

class DummyStorage(TournamentStorage):
    def update_player(self, p):
        pass
    def update_game(self, p):
        pass

def load_tournament_storage(storage_type):
    if storage_type == 'dummy':
        return DummyStorage()
    raise NotImplementedError('Storage type <{}> not supported yet'.format(storage_type))

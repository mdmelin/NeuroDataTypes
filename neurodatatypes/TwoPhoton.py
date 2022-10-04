from .data_utils import create_bhv_dataframe
from . import paths

class TwoPhoton():
    def __init__(self, datapath, animal, date):
        self.twoppath = paths.get_twop_path(self)
        self.opts = paths.get_twop_opts_path(self)
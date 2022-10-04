# -*- coding: utf-8 -*-
from . import paths

class Ephys():
    def __init__(self, datapath, animal, date):
        self.ephyspath = paths.get_ephys_path(self)
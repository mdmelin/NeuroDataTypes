from .data_utils import load_widefield_raw, load_widefield_SVD
from . import paths

class Widefield():
    def __init__(self, datapath, animal, date):
        self.datapath = datapath
        self.animal = animal
        self.date = date
        self.alVc = None
        self.segFrames = None
        self.segInx = None
        self.transParams = None

        self.optspath = paths.get_wfield_opts_path(datapath, animal, date) 
        self.wfpath = paths.get_wfield_path(datapath, animal, date)
        self.svdpath = paths.get_SVD_path(datapath, animal, date)
        
        self.raw = load_widefield_raw(self.wfpath)
        self.U, self.Vc = load_widefield_SVD(self.svdpath)
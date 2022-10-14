from .data_utils import load_widefield_raw, load_widefield_SVD, load_widefield_opts
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

        optspath = paths.get_wfield_opts_path(datapath, animal, date) 
        wfpath = paths.get_wfield_path(datapath, animal, date)
        svdpath = paths.get_SVD_path(datapath, animal, date)
        
        self.raw = load_widefield_raw(wfpath)
        self.U, self.Vc, self.frametimes, self.bpod_trials = load_widefield_SVD(svdpath)
        self.opts = load_widefield_opts(optspath)
    def align_to_behavior(self):
        
        raise NotImplementedError()
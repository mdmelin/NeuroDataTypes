from .data_loading import load_widefield_raw, load_widefield_SVD, load_widefield_opts
from . import paths
import numpy as np


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
        self.U, Vc, frametimes, self.bpod_trials, self.trials = load_widefield_SVD(svdpath)  # Vc is [dims, frames, trials]
        self.num_svd_dims, _, self.num_trials = Vc.shape
        self.times = frametimes.reshape((-1))
        self.Vc = Vc.reshape((self.num_svd_dims, -1))


if __name__ == '__main__':  # debugging use only
    data = r'X:\Widefield'
    mouse = 'mSM63'
    date = '03-Jul-2018'
    wf = Widefield(data, mouse, date)

from .data_utils import load_widefield_raw, load_widefield_SVD, load_widefield_opts
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
        self.U, self.Vc, self.frametimes, self.bpod_trials, self.trials = load_widefield_SVD(svdpath) #Vc is [dims, frames, trials]
        self.opts = load_widefield_opts(optspath)
    def align_to_behavior(self, requested_trials = None):
        if requested_trials is None:
            requested_trials = self.bpod_trials
        
        n_bpod_trials = 5000 #TODO: make this SessionData.NTrials
        included = self.trials <= n_bpod_trials #Ensure there are not too many trials in Vc 
        self.trials = self.trials[included]
        self.bpod_trials = self.bpod_trials[included]
        self.Vc = self.Vc[:,:,included]
        
        num_requested = np.size(requested_trials)
        
        good_trials = requested_trials[np.isin(requested_trials,self.bpod_trials)] #returns the requested bpod trial #'s that have imaging data
        bTrials = np.where(np.isin(self.bpod_trials,requested_trials))[0] #gives us the indices to grab from Vc
        self.Vc = self.Vc[:,:,bTrials]
        n_trials = len(bTrials)
        print('''
              Requesting {} trials from {} trials in BPod session. 
              Aligning {} trials (Vc dataset sometimes has some missing trials).
              '''.format(num_requested, n_bpod_trials, n_trials))
        
        epoch_lengths = np.array([1, 0.5, 1.00, 0.4, 0.75]) # TODO: make this a function arg
        fs = self.opts['frameRate']
        epoch_frames = np.cumsum(np.floor(epoch_lengths * fs), dtype=int) #marks the frames where each epoch begins
        
        #do the actual alignment
        rejected_count = 0
        newVc = np.full([np.shape(self.Vc)[0], epoch_frames[-1], np.shape(self.Vc)[2]], np.nan)
        
        for i in range(np.shape(self.Vc)[2]): #iterate over trials
            f = 3
            aligned_frame = self._align_one_frame() #do aligning here
            
        
        del self.Vc #TODO: delete things that are unneeded now
        raise NotImplementedError()
        return alVc, bpod_trials
    
    def _align_one_frame(self, frame, epoch_frames):
        raise NotImplementedError()
        return aligned_frame
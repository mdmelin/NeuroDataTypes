# -*- coding: utf-8 -*-
from .data_utils import load_session_dataframe, load_session_metadata
from . import paths
import os
import glob
from multiprocessing import Pool, freeze_support
from itertools import repeat
from datetime import datetime
import numpy as np

#TODO: Create Subject object and a file to save metadata to
class Session():
    def __init__(self, datapath, animal, date):

        self.datapath = datapath
        self.animal = animal
        self.date = date #TODO: Make this a datetime?
        self.data = None #only generate pandas dataframe if required.
        self.bhvpath = paths.get_behavior_path(datapath, animal, date)
        self.metadata = load_session_metadata(self.bhvpath) #TODO: maybe pin to a metadata file for quicker access
        self.data, self.stimtimes = load_session_dataframe(self.bhvpath)
    
    def get_trial_indices(self): #returns trial numbers based on desired condition
        raise NotImplementedError()
        
    def get_expected_states(self,GLMHMM): #TODO: probably move to glmhmm object
        raise NotImplementedError() 
        
    @staticmethod
    def return_dates(animal):
        '''
        This function will return session dates for an animal that satisfy
        a certain criteria. create this function after done with other methods 
        that return performance and metadata for a session.
        '''
        raise NotImplementedError()        
        
    @staticmethod
    def get_sessions(dpath, animal, max_nochoice = None, modality = None, min_trials = None, singlespout_cutoff = None, assisted_cutoff = None, discrim_min = None, discrim_max = None, min_percent_correct = None): #TODO: Make general purpose for dataset, or move it
    #TODO: get by date
        '''
        Loads all availible sessions into list in parallel
        '''
        searchdir = os.path.join(dpath,animal,'SpatialDisc')
        dates = [date for date in os.listdir(searchdir) if os.path.isdir(os.path.join(searchdir, date))] #get folders only
        
        #sessions = [Session(dpath,animal,date) for date in dates] #single process
        with Pool() as pool: #multiple processes
            sessions = pool.starmap(Session, zip(repeat(dpath), repeat(animal), dates))
        
        sessions_sorted = sorted(sessions,key=lambda session: datetime.strptime(session.date[:11], "%d-%b-%Y")) #sort sessions by date       
        
        if modality is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['modality'] == modality]
        if min_trials is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['n_trials'] >= min_trials]
        if assisted_cutoff is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['assisted'] >= assisted_cutoff]
        if discrim_min is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['discrimination'] >= discrim_min]
        if discrim_max is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['discrimination'] <= discrim_max]
        if min_percent_correct is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['percent_correct'] >= min_percent_correct]
        if singlespout_cutoff is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['singlespout_percent'] <= singlespout_cutoff]
        if max_nochoice is not None:
            sessions_sorted = [sess for sess in sessions_sorted if np.sum(np.isnan(sess.data.choice)) <= max_nochoice]

        return sessions_sorted
    

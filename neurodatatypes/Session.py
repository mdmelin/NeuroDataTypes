# -*- coding: utf-8 -*-
from .data_loading import load_session_dataframe, load_session_metadata
from . import paths
import os
import glob
from multiprocessing import Pool, freeze_support
from itertools import repeat
from datetime import datetime
import numpy as np

class Session():
    def __init__(self, datapath, animal, date):

        self.datapath = datapath
        self.animal = animal
        self.date = date
        self.data = None  # only generate pandas dataframe if required.
        self.bhvpath = paths.get_behavior_path(datapath, animal, date)
        self.metadata = load_session_metadata(self.bhvpath)
        self.data, self.stimtimes = load_session_dataframe(self.bhvpath)
    
    def get_trial_indices(self): 
        """
        returns trial numbers based on desired condition
        """
        raise NotImplementedError()
        
    def get_event_times(self, alignment_event):
        raise NotImplementedError()
        # This will return a dataframe of times relative to a specific trial event
        # dubbed alignment_event. 
        # The dataframe will probably need two levels of arrays. 
        # see encoding model to find out where this is retrieved
            
    @staticmethod
    def get_sessions(dpath,  # TODO: Make general purpose for dataset, or move it
                     animal,
                     max_nochoice=None,
                     modality=None,
                     min_trials=None,
                     singlespout_cutoff=None,
                     assisted_cutoff=None,
                     discrim_min=None,
                     discrim_max=None,
                     min_percent_correct=None):
        """_summary_

        Parameters
        ----------
        dpath : _type_
            _description_
        ormoveitanimal : _type_
            _description_
        max_nochoice : _type_, optional
            _description_, by default None
        modality : _type_, optional
            _description_, by default None
        min_trials : _type_, optional
            _description_, by default None
        singlespout_cutoff : _type_, optional
            _description_, by default None
        assisted_cutoff : _type_, optional
            _description_, by default None
        discrim_min : _type_, optional
            _description_, by default None
        discrim_max : _type_, optional
            _description_, by default None
        min_percent_correct : _type_, optional
            _description_, by default None

        Returns
        -------
        sessions_sorted: list
            a list of session objects satisfying the desired criteria, sorted by date.
        """

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
            #sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['discrimination'] >= discrim_min]
            sessions_sorted = [sess for sess in sessions_sorted if (np.sum(sess.data['discrimination']) / sess.metadata['n_trials']) >= discrim_min]
        if discrim_max is not None:
            #sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['discrimination'] <= discrim_max]
            sessions_sorted = [sess for sess in sessions_sorted if (np.sum(sess.data['discrimination']) / sess.metadata['n_trials']) <= discrim_max]
        if min_percent_correct is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['percent_correct'] >= min_percent_correct]
        if singlespout_cutoff is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['singlespout_percent'] <= singlespout_cutoff]
        if max_nochoice is not None:
            sessions_sorted = [sess for sess in sessions_sorted if np.sum(np.isnan(sess.data.choice)) <= max_nochoice]

        return sessions_sorted

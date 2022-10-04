# -*- coding: utf-8 -*-
from .data_utils import load_session_dataframe, load_session_metadata
from . import paths
import os
import glob
from multiprocessing import Pool, freeze_support
from itertools import repeat
from datetime import datetime
#TODO: Create Subject object and a file to save metadata to
class Session():
    def __init__(self, datapath, animal, date):

        self.datapath = datapath
        self.animal = animal
        self.date = date
        self.data = None #only generate pandas dataframe if required.
        self.bhvpath = paths.get_behavior_path(datapath, animal, date)
        self.metadata = load_session_metadata(self.bhvpath) #TODO: maybe pin to a metadata file for quicker access
        self.data = load_session_dataframe(self.bhvpath)
        
    def _get_expected_states(self,GLMHMM): #TODO: probably move to glmhmm object
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
    def all_sessions(dpath, animal,modality = None): #TODO: Make general purpose for dataset, or move it
        '''
        Loads all availible sessions into list in parallel
        '''
        dates = os.listdir(os.path.join(dpath,animal,'SpatialDisc'))
        #sessions = [Session(dpath,animal,date) for date in dates] #single thread
        with Pool() as pool:
            sessions = pool.starmap(Session, zip(repeat(dpath), repeat(animal), dates))
        sessions_sorted = sorted(sessions,key=lambda session: datetime.strptime(session.date[:11], "%d-%b-%Y")) #sort sessions by date       
        
        if modality is not None:
            sessions_sorted = [sess for sess in sessions_sorted if sess.metadata['modality'] == modality]
        return sessions_sorted
    

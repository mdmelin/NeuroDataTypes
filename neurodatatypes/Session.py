# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
import glob
from .data_utils import create_bhv_dataframe


EXPERIMENT = 'Widefield'
TASK = 'SpatialDisc'
SVD_FILENAME = 'Vc.mat'
OPTS_FILE_WILDCARD = 'opts*.mat'


class Session():
    def __init__(self, dPath, Animal, Rec):

        self.dpath = dPath
        self.animal = Animal
        self.date = Rec
        self.data = None #only generate pandas dataframe if required.

        searchpath = os.path.join(dPath, Animal, TASK, Rec)
        bhv_file_wildcard = '{}_{}_*_Session*.mat'.format(Animal, TASK)
        bhv_filenames = glob.glob(os.path.join(searchpath, bhv_file_wildcard))
        assert len(
            bhv_filenames) == 1, "Can't find behavior file or there are multiple."

        
        opts_filenames = glob.glob(
            os.path.join(searchpath, OPTS_FILE_WILDCARD))
        if len(opts_filenames) > 1:
            print(
                '\nThere are multiple opts files for this session, selecting the latest one.')

        optspath = os.path.join(searchpath, opts_filenames[-1])
        bhvpath = os.path.join(searchpath, bhv_filenames[0])
        svdpath = os.path.join(searchpath, SVD_FILENAME)
        ephyspath = None
        twoppath = None
        
        self.paths = {'wfield': None, 'svd': svdpath, 'opts': optspath, 'behavior': bhvpath} #Paths to all availible data

    def report_session_info():  # report back session metadata (% correct, etc.)
        raise NotImplementedError()
        
    def _get_expected_states(self,GLMHMM): #TODO: probably move to glmhmm object
        raise NotImplementedError()

    def _get_behavior_data(self):  # load behavior file into pandas dataframe
        print('\nGenerating pandas DataFrame of behavioral data for each trial.')
        self.data = create_bhv_dataframe(self.paths['behavior'])
        

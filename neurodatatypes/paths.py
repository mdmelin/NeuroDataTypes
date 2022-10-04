"""Returns paths for the session"""
import os
import glob

EXPERIMENT = 'Widefield'
TASK = 'SpatialDisc'
SVD_FILENAME = 'Vc.mat'
OPTS_FILE_WILDCARD = 'opts*.mat'
BHV_FILE_WILDCARD = '{}_{}_*_Session*.mat'

def get_behavior_path(datapath, animal, date):
    searchpath = os.path.join(datapath, animal, TASK, date)
    bhv_file_wildcard = BHV_FILE_WILDCARD.format(animal, TASK)
    bhv_filenames = glob.glob(os.path.join(searchpath, bhv_file_wildcard))
    assert len(bhv_filenames) == 1, "Can't find behavior file or there are multiple."
    bhvpath = os.path.join(searchpath, bhv_filenames[0])
    return bhvpath


def get_wfield_opts_path(datapath, animal, date):
    searchpath = os.path.join(datapath, animal, TASK, date)
    opts_filenames = glob.glob(os.path.join(searchpath, OPTS_FILE_WILDCARD))
    if len(opts_filenames) > 1:
        print('\nThere are multiple opts files for this session, selecting the latest one.')
    optspath = os.path.join(searchpath, opts_filenames[-1])
    return optspath
    
def get_SVD_path(datapath, animal, date):
    searchpath = os.path.join(datapath, animal, TASK, date)
    svdpath = os.path.join(searchpath, SVD_FILENAME)
    return svdpath

def get_wfield_path(datapath, animal, date):
    return None
    
def get_ephys_path(datapath, animal, date):
    #TODO: for IBL Data, make use of ONE cache_dir param
    return None

def get_twop_path(datapath, animal, date):
    return None






"""
By Max Melin

Data loading module which is called by the data classes. This is specific to
the data formats and paths of the user/dataset
"""
import matlab.engine
import numpy as np
import pandas as pd
from scipy.io import loadmat
from mat73 import loadmat as loadmat73

STRUCTNAME = 'SessionData'
MATLABPATH = r'C:/Data/churchland/NeuroDataTypes/matlab_functions' #TODO: make this generic, or remove if not needed

eng = matlab.engine.start_matlab()
eng.cd(MATLABPATH, nargout=0)


def load_session_dataframe(bhvpath): #return DataFrame with info for each trial
    # matfile = loadmat(bhvpath, simplify_cells = True)[STRUCTNAME]
    # numtrials = int(matfile.nTrials)
    # choice = matfile.ResponseSide - 1
    # stimside = matfile.CorrectSide - 1
    # stimtype = matfile.StimType
    # stimstruct = matfile.stimEvents #TODO: This has been removed from the dataframe because it casts the np array as an array of objects. there is probably a way to input this separately into the dataframe so it doesn't disrupt the others
    # # TODO: change this to leftstim and right stim
    # # TODO: compute reaction times? or maybe just put important times into another array
    # targstim = matfile.TargStim
    # diststim = matfile.DistStim
    # assisted = matfile.Assisted
    # singlespout = matfile.SingleSpout
    # rewarded = matfile.Rewarded
    
    #For older scipy version
    matfile = loadmat(bhvpath, simplify_cells = True)[STRUCTNAME]
    numtrials = int(matfile['nTrials'])
    choice = matfile['ResponseSide'] - 1
    stimside = matfile['CorrectSide']- 1
    stimtype = matfile['StimType']
    stimstruct = matfile['stimEvents'] #TODO: This has been removed from the dataframe because it casts the np array as an array of objects. there is probably a way to input this separately into the dataframe so it doesn't disrupt the others
    # TODO: change this to leftstim and right stim
    # TODO: compute reaction times? or maybe just put important times into another array
    targstim = matfile['TargStim']
    diststim = matfile['DistStim']
    assisted = matfile['Assisted']
    singlespout = matfile['SingleSpout']
    rewarded = matfile['Rewarded']

    
    try:
        # get the opto data if it exists
        optotype = matfile.optoType
    except AttributeError:
        optotype = np.empty(numtrials)
        optotype[:] = np.nan
    
    temparray = np.stack([choice, stimside, stimtype,
                               targstim, diststim, assisted, singlespout, 
                               rewarded, optotype])
    behavior_dataframe = pd.DataFrame(temparray.T, columns=[
                                'choice', 'stimside', 'stimtype',
                                'targstim', 'diststim', 'assistted',
                                'singlespout', 'rewarded', 'optotype'])
    return behavior_dataframe

def load_session_metadata(bhvpath): #this will return a dictionary with modality and other metadata (things that span all trials)
    #TODO: add more metadata
    matfile = loadmat(bhvpath, simplify_cells = True)[STRUCTNAME]
    numtrials = int(matfile['nTrials'])
    modality = np.mean(matfile['StimType']) #TODO: make this better... call modality by a word
    
    metadata_dict = {'modality': modality}
    return metadata_dict

def load_widefield_SVD(SVDpath): #return SVD components
    matfile = loadmat73(SVDpath)
    U = matfile['U']
    Vc = matfile['Vc']
    return U,Vc

def load_widefield_raw(Session): #return raw widefield data 
    return None
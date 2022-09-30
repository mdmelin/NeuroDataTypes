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

eng = matlab.engine.start_matlab()
eng.cd(r'C:/Data/churchland/NeuroDataTypes/matlab_functions',
       nargout=0)  # TODO: make this generic


def create_bhv_dataframe(bhvpath): #return DataFrame with info for each trial
    matfile = loadmat(bhvpath)[STRUCTNAME]
    numtrials = int(matfile['nTrials'])
    choice = matfile['ResponseSide'][0, 0] - 1
    stimside = matfile['CorrectSide'][0, 0] - 1
    stimtype = matfile['StimType'][0, 0]
    stimstruct = matfile['stimEvents'][0, 0]
    # TODO: change this to leftstim and right stim
    targstim = matfile['TargStim'][0, 0]
    diststim = matfile['DistStim'][0, 0]
    assisted = matfile['Assisted'][0, 0]
    singlespout = matfile['SingleSpout'][0, 0]
    rewarded = matfile['Rewarded'][0, 0]
    try:
        # get the opto data if it exists
        optotype = matfile['optoType'][0, 0]
    except ValueError:
        optotype = np.empty((1, numtrials))
        optotype[:, :] = np.nan
    
    temparray = np.concatenate((choice, stimside, stimtype, stimstruct,
                               targstim, diststim, assisted, singlespout, 
                               rewarded, optotype))
    behavior_dataframe = pd.DataFrame(temparray.T, columns=[
                                'choice', 'stimside', 'stimtype', 'stimstruct',
                                'targstim', 'diststim', 'assistted',
                                'singlespout', 'rewarded', 'optotype'])
    return behavior_dataframe

def load_widefield_SVD(SVDpath): #return SVD components
    matfile = loadmat73(SVDpath)
    U = matfile['U']
    Vc = matfile['Vc']
    return U,Vc

def load_widefield_raw(Session): #return raw widefield data 
    return None
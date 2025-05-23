"""
By Max Melin

Data loading module which is called by the data classes. This is specific to
the data formats and paths of the user/dataset
"""

import numpy as np
import pandas as pd
from scipy.io import loadmat
from mat73 import loadmat as loadmat73

STRUCTNAME = 'SessionData'
MATLABPATH = r'C:/Data/churchland/NeuroDataTypes/matlab_functions' # TODO: make this generic, or remove if not needed

# import matlab.engine
# eng = matlab.engine.start_matlab()
# eng.cd(MATLABPATH, nargout=0)


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
    distractor_probability = np.array([settingsdict['DistProb'] for settingsdict in matfile['TrialSettings']]) #if set to 1 indicates discrimination is being delivered
    distractor_fractions_length = np.array([np.size(settingsdict['DistFractions']) for settingsdict in matfile['TrialSettings']])
    discrimination_boolean = np.logical_and(np.where(distractor_probability==1, 1, 0), np.where(distractor_fractions_length >= 4, 1,0))
    
    try:
        # get the opto data if it exists
        optotype = matfile.optoType
    except AttributeError:
        optotype = np.empty(numtrials)
        optotype[:] = np.nan
    
    temparray = np.stack([choice, stimside, stimtype,
                               targstim, diststim, assisted, singlespout, 
                               rewarded, optotype, discrimination_boolean])
    behavior_dataframe = pd.DataFrame(temparray.T, columns=[
                                'choice', 'stimside', 'stimtype',
                                'targstim', 'diststim', 'assistted',
                                'singlespout', 'rewarded', 'optotype', 'discrimination'])
    return behavior_dataframe, stimstruct

def load_session_metadata(bhvpath): #this will return a dictionary with modality and other metadata (things that span all trials)
    #TODO: add more metadata
    matfile = loadmat(bhvpath, simplify_cells = True)[STRUCTNAME]
    n_trials = int(matfile['nTrials'])
    modality = np.mean(matfile['StimType']) #TODO: make this better... call modality by a word
    assisted = np.mean(matfile['Assisted'])
    discrimination = np.mean(matfile['DistStim'] > 0)
    percent_correct = np.mean(matfile['CorrectSide'] == matfile['ResponseSide'])
    singlespout_percent = np.mean(matfile['SingleSpout'])
    metadata_dict = {'modality': modality,
                     'n_trials': n_trials,
                     'assisted': assisted,
                     'discrimination': discrimination,
                     'percent_correct': percent_correct,
                     'singlespout_percent': singlespout_percent
                     }
    return metadata_dict

def load_widefield_SVD(SVDpath): #return SVD components
    matfile = loadmat73(SVDpath)
    U = matfile['U']
    Vc = matfile['Vc']
    frametimes = matfile['blueFrametimes']
    bpod_trials = matfile['bTrials'] #bpod trial numbers that have widefield data
    trials = matfile['trials']

    bpod_trials = bpod_trials - 1 # ESSENTIAL LINE, WE MOVE THE BPOD TRIAL INDICES DOWN BY ONE SINCE WE'RE CONVERTING FROM MATLAB TO PYTHON
    trials = trials - 1
    
    return U, Vc, frametimes, bpod_trials, trials

def load_widefield_opts(optspath):
    matfile = loadmat(optspath, simplify_cells=True)
    from fnmatch import fnmatch
    optskey = [key for key in [*matfile] if fnmatch(key,'opts*')][0]
    opts = matfile[optskey]
    return opts

def load_widefield_raw(Session): #return raw widefield data 
    return None
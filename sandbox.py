# -*- coding: utf-8 -*-


from neurodatatypes import *
from sklearn.decomposition import PCA
import numpy as np
#%% Lets try to plot a heatmap
data = 'X:\Widefield'
mouse = 'mSM63'
date = '03-Jul-2018'

session = Session(data,mouse,date) # TODO: somehow grab sessions with min number of trials in each state
wf = Widefield(data,mouse,date)

trials = np.array([0,1,2,3,4,5,6,7,154,300,301,302]) #start from zero
wf.align_to_behavior(requested_trials=trials)



#%%

### DO NOT CONFUSE INDEXING BETWEEN MATLAB AND PYTHON

"""
The general order should be as follows.

1. Get the desired trial #'s for performing a manipulation or analysis

2. From those trial #'s grab the time aligned imaging data.
Also return corresponding behavior data. 

(unSVD and align to allen before analysis, unshrink array as late as possible)

3. Perform desired analysis

(or unSVD and align to allen after analysis, unshrink array as late as possible)
"""
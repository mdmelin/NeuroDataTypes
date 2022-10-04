# -*- coding: utf-8 -*-


from neurodatatypes import *
from sklearn.decomposition import PCA
import numpy as np
#%% Lets try to plot a heatmap
data = 'X:\Widefield'
mouse = 'mSM63'
date = '03-Jul-2018'

session = Session(data,mouse,date)
session._get_behavior_data()
wf = Widefield(data,mouse,date)


## DO NOT CONFUSE INDEXING BETWEEN MATLAB AND PYTHON

"""
The general order should be as follows.

1. Get the desired trial #'s for performing a manipulation or analysis

2. From those trial #'s grab the time aligned imaging data.
Also return corresponding behavior data. 

(unSVD and align to allen before analysis, unshrink array as late as possible)

3. Perform desired analysis

(or unSVD and align to allen after analysis, unshrink array as late as possible)
"""
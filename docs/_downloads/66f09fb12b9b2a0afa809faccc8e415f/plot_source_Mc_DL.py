"""
Resampling posteriors
=====================

Convert sampling parameters to derived parameters
"""

#%%
# This example shows how to change parameterization of the posterior samples. 
# The GBMCMC sampler uses frequency, frequency derivative, and GW amplitude in its waveform model. 
# For systems whose dynamics are driven by GR, those parameters can be converted to chirp mass and luminosity distance. 
# Here is a demonstration of how to do that by producing a chirpmass-distance corner plot.

# Import modules
import os
import pandas as pd
from chainconsumer import ChainConsumer
import lisacattools.lisacattools as lisacat

# Start by loading the main catalog file processed from GBMCMC outputs
catFile = 'cat15728640_v2/cat15728640_v2.h5'
catPath = os.path.split(catFile)[0]
cat = pd.read_hdf(catFile, key='detections')

# Sort table by SNR and select highest SNR source
cat.sort_values(by='SNR',ascending = False, inplace=True)
sourceId = cat.index[0]
samples = lisacat.getChain(cat,sourceId,catPath)

# Reject chain samples with negative fdot (enforce GR-driven prior)
samples_GR = samples[(samples['Frequency Derivative']> 0)]

# Add distance and chirpmass to samples
lisacat.get_DL(samples_GR)
lisacat.get_Mchirp(samples_GR)

# Make corner plot
parameters = ['Chirp Mass','Luminosity Distance']
parameter_symbols = [r'$\mathcal{M}\ [{\rm M}_\odot]$',
                   r'$D_L\ [{\rm kpc}]$']

df = samples_GR[parameters].values

c = ChainConsumer().add_chain(df,parameters=parameter_symbols,cloud=True)
c.configure(flip=False)
fig=c.plotter.plot(figsize=1.5)

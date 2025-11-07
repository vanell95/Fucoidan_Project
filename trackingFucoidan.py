#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 12:12:44 2024

@author: keegstra
"""

import trackpy as tp
import numpy as np
import TrackpyBact as tpb
from nd2reader import ND2Reader
import cv2
import matplotlib as plt
import seaborn as sns
import pandas as pd
import os
import pickle
import matplotlib.pyplot as plt 

#%%
filepath='/Users/keegstra/Desktop/240806/Pseudoalteromonas/ASV16_1/'
filename='ASV16_ASW_1'

with ND2Reader(filepath+filename+'.nd2') as ImageStack:
    Nframes=ImageStack.sizes['t']
    FPS=1000/np.mean((np.diff(ImageStack.timesteps)))
    MED=tpb.fixedBackgroundCorrection(ImageStack)
    correction_method='med bck subtraction'
    #MED=movingBackgroundCorrection(ImageStack,time_window)
    voxel_size=ImageStack.metadata['pixel_microns']
    #TimeSeries=np.zeros_like(ImageStack)
    TimeSeries_C=np.zeros_like(ImageStack)
    for ii in range(Nframes):
        TimeSeries_C[ii]=np.add(np.absolute(np.subtract(ImageStack[ii].astype(int),MED)),1000).astype('uint16'); #toggle toMED[ii]     
          
ImageStack=[]

#%%

IMG=TimeSeries_C[0]
p=tp.locate(IMG,11,separation=41,minmass=2000)

plt.figure(1)
plt.hist(p['mass'],100)

plt.figure(2)
plt.subplot(1,2,1)
tp.annotate(p,IMG,imshow_style={'vmin':900,'vmax':1500})
plt.gca().invert_yaxis()

IMG=TimeSeries_C[0]
p=tp.locate(IMG,5,separation=41,minmass=300)
plt.subplot(1,2,2)
tp.annotate(p,IMG,imshow_style={'vmin':900,'vmax':1500})
plt.gca().invert_yaxis()

#%%
plt.figure(3)
plt.imshow(IMG,vmin=900,vmax=1250)



#%%

datafiles=[s for s in os.listdir('C:/Users/Anelli/Desktop/Experiments/Tracking_experiments/20241108_20240828') if s.endswith('pickle')]
#datafiles=[s for s in datafiles if s.__contains__('20240405')]

time=[]
q=[]
kk=0
plt.figure(3)
for ff in datafiles:
    strainname=ff.split('_')[1].split('.')[0]
    date=ff.split('_')[0]
    with open('C:/Users/Anelli/Desktop/Experiments/Tracking_experiments/20241108_20240828/'+ff,'rb') as f:
        trackingResults=pickle.load(f)
    nvids=len(trackingResults)
    filenames=[trackingResults[ii]['metadata']['filename'] for ii in range(nvids)]
    timedat=[filenames[i].split('/')[1].split('_')[1] for i in range(len(filenames))]
    concentrations=[float(s.replace('ASW','0')) for s in timedat]
    expID=[filenames[i].split('_')[-1] for i in range(len(filenames))]
    #times,condition,time_units=getTimeFromFileName(filenames)
    zpos=filenames[0].split('/')[0]
    for vv in range(nvids):
        cProp=trackingResults[vv]['cProp']
        avgSpeedCell=np.nanmean(cProp['speeds5'])
        ntrajs=len(cProp['speeds5'])
        avgSpeedMotCell=np.nanmean(cProp[cProp['motile?']==1]['speeds5'])
        fastFrac=cProp.loc[(cProp['motile?']==1)&(cProp['speeds5']>45)].count()/cProp.count()
        nturns=trackingResults[vv]['traj_analysed'].groupby('particle').mean()['turn_Ntot'].dropna()
        angles=trackingResults[vv]['traj_analysed'].groupby('particle').mean()['turn_angle'].tolist()
        turnfreqs_cs=(1./trackingResults[vv]['traj_analysed'].groupby('particle').mean()['run_time_sloppy'])
        turnfreqs_csf=np.array(turnfreqs_cs)[np.array(angles)>90]
        q.append(
            {
            'strain':strainname,
            'expID':expID[vv],
            'fuc':concentrations[vv],
            'zpos':zpos,
            'ntrajs':ntrajs,
            'date':date,
            'speeds5':trackingResults[vv]['traj_analysed']['speeds_sg'].mean(),
            'turnFreq_cs':(1./trackingResults[vv]['traj_analysed'].groupby('particle').mean()['run_time_sloppy']).mean(),
            'motFrac':trackingResults[vv]['cProp']['motileFrac'][0],
            'avgSpeedFastest':np.percentile(trackingResults[vv]['cProp']['speeds5'],90), #10% fastest cells
            'avgSpeedMotCell':avgSpeedMotCell,
            }
            )
        #plt.subplot(3,3,vv+1)
        #plt.hist(trackingResults[vv]['traj_analysed'].groupby('particle').mean()['speeds5'],range=[0,60],bins=30)
    kk=kk+1   

dF=pd.DataFrame(q)
#%%
plt.figure(1); plt.clf()
plt.subplot(131)
sns.lineplot(data=dF,x='fuc',y='motFrac', linewidth=5)
plt.plot([0.001,10],[dF.loc[dF['fuc']==0,'motFrac'].mean(),dF.loc[dF['fuc']==0,'motFrac'].mean()])
plt.gca().set_xscale('log')
plt.ylim(0,1)
plt.xlabel('fucoidan concentration (mg/mL)')
plt.ylabel('fraction of motile cells(%)')

plt.subplot(132)
sns.lineplot(data=dF,x='fuc',y='avgSpeedMotCell',linewidth=5)
plt.plot([0.001,10],[dF.loc[dF['fuc']==0,'avgSpeedMotCell'].mean(),dF.loc[dF['fuc']==0,'avgSpeedMotCell'].mean()])
plt.gca().set_xscale('log')
plt.ylim(20,80)
plt.xlabel('fucoidan concentration (mg/mL)')
plt.ylabel('average speed of motile cells (µm/sec)')


plt.subplot(133)
sns.lineplot(data=dF,x='fuc',y='turnFreq_cs',linewidth=5)
plt.plot([0.001,10],[dF.loc[dF['fuc']==0,'turnFreq_cs'].mean(),dF.loc[dF['fuc']==0,'turnFreq_cs'].mean()])
plt.gca().set_xscale('log')
plt.ylim(1,5)
plt.xlabel('fucoidan concentration (mg/mL)')
plt.ylabel('Reorientation frequency (1/s)')

plt.rcParams['axes.labelsize'] = 50 # Set default axis label size
plt.rcParams['xtick.labelsize'] = 50  # Set default x-tick label size
plt.rcParams['ytick.labelsize'] = 50 

#%%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(20, 20))
sns.lineplot(data=dF, x='fuc', y='motFrac', linewidth=8)

# Plot horizontal line at mean motility for fuc == 0
mean_motFrac_fuc0 = dF.loc[dF['fuc'] == 0, 'motFrac'].mean()
plt.plot([0.001, 10], [mean_motFrac_fuc0, mean_motFrac_fuc0], 
         color='gray', linestyle='-', linewidth=10, label='ASW')

plt.xscale('log')
plt.ylim(0, 1)  # Adjust if motFrac is percentage (use 0,100 instead)
plt.xlabel('Fucoidan concentration (mg/mL)')
plt.ylabel('Fraction of motile cells')


plt.legend(prop={'size': 50},loc='upper right')
plt.tight_layout()
plt.show()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 12:32:49 2019

@author: nikonalesheo
"""

import os 
import numpy as np

def sched_source_write(file, source, DEC_median, time_source, up = False):  

    ### looking foe dwell ###
    
    # Number of scans upper or below median value of DEC for all sources
    N_scans_up = 8
    N_scans_down = 6
    
    if up == True:
        dwell = int(time_source//N_scans_up)
        file.write( "source = '"+source+"' dwell = "+str(dwell)+"/"+'\n')
    
    else:
        if float(source[5:10])<DEC_median:
            dwell = int(time_source//N_scans_down)
        else:
            dwell = int(time_source//N_scans_up)
        
        file.write( "source = '"+source+"' dwell = "+str(dwell)+"/"+'\n')
    
    return dwell
    ### end of looking dwell ###   
   
    

name = 'YY.list'

sources_list = np.loadtxt(name, dtype = 'object', usecols = 0)
N_sources = len(sources_list)

RA = np.zeros(N_sources)
DEC = np.zeros(N_sources)

for i in range(N_sources):
    RA[i] = float(sources_list[i][1:5])
    DEC[i] = float(sources_list[i][5:10])

DEC_median = np.median(DEC)

G1 = sources_list[::2]
G2 = sources_list[1::2]

#time_tot = (24-7.62)*60*60
#time_tot = 2*(24-9.12)*60*60
time_tot = 2*(24-4.6)*60*60
time_source = time_tot/N_sources

phi_SC = np.deg2rad(17.75658)
lambda_SC = np.deg2rad(64.58363)
phi_MK = np.deg2rad(19.80139)
lambda_MK = np.deg2rad(155.45551)
lambda_PT = np.deg2rad(108.11919)

delta_SC = lambda_SC - lambda_PT 
delta_MK = lambda_MK - lambda_PT
 
LST_PT = 0
n = 0
file = open('SCMK_'+name+'.sched_slist', 'w')
k = 0
while LST_PT<=24*60*60:
    
    file.write("!Cycle "+str(n) + '\n')
    t_scan = 0
#    print('Cycle')
    for i in range(len(G1)):
        
        alpha = np.deg2rad((float(G1[i][1:3]) + float(G1[i][3:5])/60)*15)
        delta = np.deg2rad(float(G1[i][5:8])+float(G1[i][8:10])/60)
        
#        print('Source = '+G1[i]+' '+str(np.rad2deg(alpha))+' '+str(np.rad2deg(delta)))
        
        t_SC = np.deg2rad((LST_PT/60/60)*15) + delta_SC - alpha
        t_MK = np.deg2rad((LST_PT/60/60)*15) + delta_MK - alpha
        
        if t_SC < 0:
            while t_SC < 0:
                t_SC = t_SC + 2*np.pi
        elif t_SC > 2*np.pi:
            while t_SC > 2*np.pi:
                t_SC = t_SC - 2*np.pi
                
        if t_MK < 0:
            while t_MK < 0:
                t_MK = t_MK + 2*np.pi
        elif t_MK > 2*np.pi:
            while t_MK > 2*np.pi:
                t_MK = t_MK - 2*np.pi       
#        print('SC '+str(np.rad2deg(t_SC))+' MK '+str(np.rad2deg(t_MK)))
        
        t_horizon_SC = np.arccos(-np.tan(delta)*np.tan(phi_SC))
        t_horizon_MK = np.arccos(-np.tan(delta)*np.tan(phi_MK))
        
#        print('SC hor'+str(np.rad2deg(t_horizon_SC))+' MK hor'+str(np.rad2deg(t_horizon_MK)))
        if t_SC < 0:
            t_SC = 2*np.pi-t_SC
        if t_MK < 0:
            t_MK = 2*np.pi-t_MK
            
        cond_SC = False 
        cond_MK = False
        
        if (t_SC < t_horizon_SC) or (t_SC > 2*np.pi - t_horizon_SC):
            cond_SC = True

        if (t_MK < t_horizon_MK) or (t_MK > 2*np.pi - t_horizon_MK):
            cond_MK = True
        
#        if i==0 or i == 20:
#                print('SC '+str(np.rad2deg(t_SC))+' MK '+str(np.rad2deg(t_MK)))
#                print(str(i)+' SC hor'+str(np.rad2deg(t_horizon_SC))+' MK hor'+str(np.rad2deg(t_horizon_MK)))
        
#        if ( (abs(t_SC)<abs(t_horizon_SC) ) and 
#               (abs(t_MK)<abs(t_horizon_MK) )  ):
        
        if cond_MK and cond_SC:  
            
            dwell = sched_source_write(file, G1[i], DEC_median, time_source)
#            t_scan = t_scan + dwell + 1.2*60
            LST_PT = LST_PT + dwell + 1.7*60
            k=k+1
            
        else:
            file.write('!')
            sched_source_write(file, G1[i], DEC_median, time_source)
            dwell = 0
#            t_scan = t_scan + dwell 
            
        
        
        
            
#    LST_PT = LST_PT + t_scan
    print('LST '+str(LST_PT)+ ' t_scan ' + str(t_scan))
    
    
    n = n + 1    


print('Cycles '+str(n))
#for i in range(len(G1)):
#    sched_source_write(file, G1[i], DEC_median, time_source)

file.close()
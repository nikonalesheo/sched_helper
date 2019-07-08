#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 18:05:10 2019

@author: nikonalesheo
"""

import mlrose 
import numpy as np

def sched_source_write(file, source, DEC_median, time_source, up = False):  
    # This function writes a line to output file. 
    
    ### looking for dwell ###
    
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
    
    ### end of looking dwell ###   

def salesman(Y):
    # This function calculate optimized order of sources to observe.
    N_sources = len(Y)

    #From name of source one can obtain RA and DEC 
    #(e.g.J0012+0267->RA = 00h 12m, DEC = 02deg 12min)
    #RA = float(Y[i][1:5])
    #DEC = float(Y[i][5:10])
    
    coords_list = []
    
    for i in range(N_sources):
        RA_h = float(Y[i][1:3])*60 # hours convert to minutes
        RA_m = float(Y[i][3:5]) # minutes
        RA = (RA_h+RA_m)*0.25 # 0.25 is degrees per hour (RA to degrees convertion)
        DEC = float(Y[i][5:8]) + float(Y[i][8:10])/60 # converted minutes to degrees
        coords_list.append((RA, DEC)) #creating a list of tuples for TSP0pt
    
    problem_fit = mlrose.TSPOpt(length = N_sources, coords = coords_list,
                                   maximize=False)
    
    best_state, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob = 0.2, 
    					      max_attempts = 100, random_state = 2)

    return best_state


# There one can put the name of a file containing list of sources
#name = 'YY.list'
name = 'Y.list'

sources_list = np.loadtxt(name, dtype = 'object', usecols = 0)
N_sources = len(sources_list)

RA = np.zeros(N_sources)
DEC = np.zeros(N_sources)

for i in range(N_sources):
    RA[i] = float(sources_list[i][1:5])
    DEC[i] = float(sources_list[i][5:10])

DEC_median = np.median(DEC)

#Time of total observing without the time of aiming to sources.
#time_tot = (24-7.62)*60*60
time_tot = (24-9.12)*60*60
time_source = time_tot/N_sources

#deviding for 8 groups by 3 hours in RA

n_groups = 8
group_n = (N_sources-1)//n_groups
group_n_left = N_sources%n_groups

file = open(name+'.sched_slist', 'w')

for n_g in range(n_groups+1): 
    if n_g == 0:
        print('group '+ str(n_g) + 's '+str((n_g-1)*group_n)+ ' ' + str(n_g*group_n))
        group_list = salesman(sources_list[0:group_n])
        file.write( "group="+str(len(group_list))+" repeat=6"+'\n')
        for i in group_list:          
            sched_source_write(file, sources_list[0:group_n][i], 
                               DEC_median, time_source)
        for j in range(1):
            file.write( "!2 scans for DEC>DEC_median to reach 8 scans"+'\n')
            for i in group_list:          
                sched_source_write(file, sources_list[0:group_n][i], 
                                   DEC_median, time_source, True)
    elif n_g == n_groups+1:
        print('group '+ str(n_g) + 's '+str((n_g-1)*group_n)+ ' ssss' + str(n_g*group_n))
        group_list = salesman(sources_list[(n_g-1)*group_n:N_sources-1])
        file.write( "group="+str(len(group_list))+" repeat=6"+'\n')
        for i in group_list:          
            sched_source_write(file, sources_list[(n_g-1)*group_n:N_sources-1][i], 
                               DEC_median, time_source)
                
        for j in range(1):
            file.write( "!2 scans for DEC>DEC_median to reach 8 scans"+'\n')
            for i in group_list:          
                sched_source_write(file, sources_list[(n_g-1)*group_n:N_sources-1][i], 
                                   DEC_median, time_source, True)
    else:
        print('group '+ str(n_g) + 's '+str((n_g-1)*group_n)+ ' ' + str(n_g*group_n))
        group_list = salesman(sources_list[n_g*group_n:(n_g+1)*group_n])
        file.write( "group="+str(len(group_list))+" repeat=6"+'\n')
        for i in group_list:          
            sched_source_write(file, sources_list[n_g*group_n:(n_g+1)*group_n][i], 
                               DEC_median, time_source)
        for j in range(1):
            file.write( "!2 scans for DEC>DEC_median to reach 8 scans"+'\n')
            for i in group_list:          
                sched_source_write(file, sources_list[n_g*group_n:(n_g+1)*group_n][i], 
                                   DEC_median, time_source, True)

file.close()

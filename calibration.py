# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 00:30:25 2019

@author: Matthew

Calibration algorthm as specified in Chapter 3.4 of 
"A Study of Polar Dust Loading from 2007 to 2019 using Satellite Thermal Data" by Matthew Bowen
"""
import numpy as np

def calibrate_image(rad_coeffs4, rad_coeffs5, cal_coeffs, scans, c4_qual, c5_qual):
    for i in range(len(scans['b4_counts'])):
        if c4_qual[i] == 128:
            scans['b4_counts'][i] = invalid_scan(scans['b4_counts'][i])
        else:
            scans['b4_counts'][i] = calibrate_row(cal_coeffs['IR4_a0'][i],
                                              cal_coeffs['IR4_a1'][i],
                                              cal_coeffs['IR4_a2'][i],
                                              scans['b4_counts'][i],
                                              rad_coeffs4)
    for i in range(len(scans['b5_counts'])):
        if c5_qual[i] == 128:
            scans['b5_counts'][i] = invalid_scan(scans['b5_counts'][i])
        else:
            scans['b5_counts'][i] = calibrate_row(cal_coeffs['IR5_a0'][i],
                                              cal_coeffs['IR5_a1'][i],
                                              cal_coeffs['IR5_a2'][i],
                                              scans['b5_counts'][i],
                                              rad_coeffs5)
    return scans

def invalid_scan(row):
    for i, c in enumerate(row):
        row[i] = 1
    return row
        
def calibrate_row(a0,a1,a2,row,rad_coeffs):
    #satellite specific coefficients
    #listed as "Thermal Channel Temperature-to-Radiance Coefficients
    #vc is central wavenumber of each band
    vc = rad_coeffs[0]
    A = rad_coeffs[1]
    B = rad_coeffs[2]
        
    #Planck's radiation constants
    c1 = 1.1910427e-5 # mW/(m^2 - sr - cm^(-4)) 
    c2 = 1.4387752 # cm - k
    #from page 7-8 (283) in NOAA KLM User's Guide
    
    for i, c in enumerate(row):
        c = a0 + a1*c + a2*np.power(c,2)
        row[i] = A + B*((c2*vc)/np.log(1 + ((c1*np.power(vc,3))/c)))
    return row
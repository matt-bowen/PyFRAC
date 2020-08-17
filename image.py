# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 19:09:58 2019

@author: Matthew

Image class. Requires gdal to pull the data records 
"""
import numpy as np
import gdal
import dtypes

class image:
    def __init__(self, filename):
        self.filename = filename
        
    def get_metadata(self):
        with open(self.filename) as f:
            f.seek(512, 0)
            head = np.fromfile(f, dtype=dtypes.header, count=1)[0]
        return head
    
    def get_coefficients(self):
        with open(self.filename) as f:
            f.seek(512, 0)
            head = np.fromfile(f, dtype=dtypes.header, count=1)[0]
            f.seek(16384, 0) 
            scans = np.fromfile(f, dtype=dtypes.scanline, count=head["count_of_data_records"])

        return {'IR4_a0' : scans["ir_operational_cal_ch_4_coefficient_1"]/(10**6),
                'IR4_a1' : scans["ir_operational_cal_ch_4_coefficient_2"]/(10**6),
                'IR4_a2' : scans["ir_operational_cal_ch_4_coefficient_3"]/(10**7),
                'IR5_a0' : scans["ir_operational_cal_ch_5_coefficient_1"]/(10**6),
                'IR5_a1' : scans["ir_operational_cal_ch_5_coefficient_2"]/(10**6),
                'IR5_a2' : scans["ir_operational_cal_ch_5_coefficient_3"]/(10**7)}
        
    def get_quality_indicators(self):
        with open(self.filename) as f:
            f.seek(512, 0)
            head = np.fromfile(f, dtype=dtypes.header, count=1)[0]
            f.seek(16384, 0) 
            scans = np.fromfile(f, dtype=dtypes.scanline, count=head["count_of_data_records"])
        return {"quality_indicator_bit_field": scans["quality_indicator_bit_field"],
                "scan_line_quality_flags": scans["scan_line_quality_flags"],
                "calibration_quality_flags": scans["calibration_quality_flags"]}
          
    def get_data_counts(self):
        dataset = gdal.Open(self.filename, gdal.GA_ReadOnly)
        band4 = dataset.GetRasterBand(4)
        band5 = dataset.GetRasterBand(5)
        return {'b4_counts' : np.array(band4.ReadAsArray()).astype(float),
                'b5_counts' : np.array(band5.ReadAsArray()).astype(float)}

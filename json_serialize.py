# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 19:22:33 2019

@author: Matthew
"""

import numpy as np
import os, sys, time, json
import dtypes
from image import image

def main():
    in_directory_str = "F:\Thesis\Images\Order 3405494805\\"
    out_directory_str = "F:\Thesis\JSON\Order 3405494805\\"
    
    with os.scandir(in_directory_str) as it:
        for entry in it:
            if entry.is_file():
                im = image(in_directory_str + entry.name)
                metadata = im.get_metadata()
                ca_coeffs = im.get_coefficients()
                data_counts = im.get_data_counts()
                
                d = {}
                d['metadata'] = {'data_set_name':str(metadata['data_set_name']).replace("'","")[1:],
                                 'noaa_spacecraft_identification_code':int(metadata['noaa_spacecraft_identification_code']),
                                 'start_of_data_set_year':int(metadata['start_of_data_set_year']),
                                 'start_of_data_set_day_of_year':int(metadata['start_of_data_set_day_of_year']),
                                 'start_of_data_set_utc_time_of_day':int(metadata['start_of_data_set_utc_time_of_day']),
                                 'end_of_data_set_year':int(metadata['end_of_data_set_year']),
                                 'end_of_data_set_day_of_year':int(metadata['end_of_data_set_day_of_year']),
                                 'end_of_data_set_utc_time_of_day':int(metadata['end_of_data_set_utc_time_of_day']),
                                 'count_of_data_records':int(metadata['count_of_data_records']),
                                 'count_of_calibrated,_earth_located_scan_lines':int(metadata['count_of_calibrated,_earth_located_scan_lines']),
                                 'count_of_missing_scan_lines':int(metadata['count_of_missing_scan_lines']),
                                 'count_of_data_gaps':int(metadata['count_of_data_gaps'])}
                d['constants'] = {'ch4':{'ch_4_central_wavenumber':float(metadata['ch_4_central_wavenumber']/(10**3)),
                                         'ch_4_constant_1':float(metadata['ch_4_constant_1']/(10**5)),
                                         'ch_4_constant_2':float(metadata['ch_4_constant_2']/(10**6))},
                                  'ch5':{'ch_5_central_wavenumber':float(metadata['ch_5_central_wavenumber']/(10**3)),
                                         'ch_5_constant_1':float(metadata['ch_5_constant_1']/(10**5)),
                                         'ch_5_constant_2':float(metadata['ch_5_constant_2']/(10**6))}}
                d['data'] = {'ch4':{'coeffs':{'IR4_a0':ca_coeffs['IR4_a0'].tolist(),
                                              'IR4_a1':ca_coeffs['IR4_a1'].tolist(),
                                              'IR4_a2':ca_coeffs['IR4_a2'].tolist()},
                                    'counts':data_counts['b4_counts'].tolist()},
                             'ch5':{'coeffs':{'IR5_a0':ca_coeffs['IR5_a0'].tolist(),
                                              'IR5_a1':ca_coeffs['IR5_a1'].tolist(),
                                              'IR5_a2':ca_coeffs['IR5_a2'].tolist()},
                                    'counts':data_counts['b5_counts'].tolist()}}
                #print(metadata['data_set_name'])
                with open(out_directory_str + str(metadata['data_set_name']).replace("'","")[1:] + '.json', 'w') as outfile:
                    json.dump(d, outfile, indent=4)
        #return d
                
    
    '''
    filename = os.path.join(os.getcwd(), "NSS.FRAC.M2.D19151.S2247.E0030.B6545556.SV")
    #files = get_all_files_in_dir()
    
    test_image = image(filename)
    #for image in files
    
    metadata = test_image.get_metadata()
    rad_to_temp_coeffs4 = [metadata['ch_4_central_wavenumber']/(10**3),
                           metadata['ch_4_constant_1']/(10**5),
                           metadata['ch_4_constant_2']/(10**6)]
    rad_to_temp_coeffs5 = [metadata['ch_5_central_wavenumber']/(10**3),
                           metadata['ch_5_constant_1']/(10**5),
                           metadata['ch_5_constant_2']/(10**6)]
    cal_coeffs = test_image.get_coefficients()
    data_counts = test_image.get_data_counts()
    '''
    
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start, 'seconds')
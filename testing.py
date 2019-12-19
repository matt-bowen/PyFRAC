import time, datetime, csv
import numpy as np
import os
from image import image
import calibration

def stats(image):
    dust_pixels = image[image < 0]
    return {'total_dust_pixels' : dust_pixels.size,
            'mean_dust_pixel_value' : np.mean(dust_pixels),
            'std_dust_pixel_value' : np.std(dust_pixels),
            'percent_dust_pixels' : dust_pixels.size/image.size}

start = time.time()
np.seterr(all='ignore')

path, dirs, files = next(os.walk("F:\Thesis\Images\Antarctic\\2018-2019"))
print(f"Found {len(files)} files.")
a = []

for i, j in enumerate(files):
	print(f"Processing file: {i+1} of {len(files)} - {j}", end="\r")

	filedata = image(path+"\\"+j)
	metadata= filedata.get_metadata()
	quality = filedata.get_quality_indicators()
	c4_cal_quality = quality['calibration_quality_flags'][:,1]
	c5_cal_quality = quality['calibration_quality_flags'][:,2]
	rad_to_temp_coeffs4 = [metadata['ch_4_central_wavenumber']/(10**3),
	metadata['ch_4_constant_1']/(10**5),
	metadata['ch_4_constant_2']/(10**6)]
	rad_to_temp_coeffs5 = [metadata['ch_5_central_wavenumber']/(10**3),
	metadata['ch_5_constant_1']/(10**5),
	metadata['ch_5_constant_2']/(10**6)]

	cal_coeffs = filedata.get_coefficients()
	data_counts = filedata.get_data_counts()
	data_counts = calibration.calibrate_image(rad_to_temp_coeffs4, rad_to_temp_coeffs5, cal_coeffs, data_counts, c4_cal_quality, c5_cal_quality)
	subtracted = data_counts['b4_counts'] - data_counts['b5_counts']
	s = stats(subtracted)
	a.append([j,metadata['start_of_data_set_year'],metadata['start_of_data_set_day_of_year'],
		metadata["start_of_data_set_utc_time_of_day"],
		subtracted.size,s['total_dust_pixels'],s['mean_dust_pixel_value'],s['std_dust_pixel_value']])

with open('2018-2019.csv', 'w', newline='') as outfile:
	wr = csv.writer(outfile)
	wr.writerows(a)
print(f"\nTotal time elapsed for {len(files)} files: {datetime.timedelta(seconds=time.time() - start)}s")
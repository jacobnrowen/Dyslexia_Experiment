import parselmouth
import numpy as np
import pandas as pd
import glob
import math

def find_peak_prom(tensity):
	cur_time = 0.0
	cur_peak_time = 0.0
	cur_peak_val = tensity.get_value(cur_time)
	while cur_time < tensity.duration:
		cur_time += 0.01
		prom = tensity.get_value(cur_time)
		if prom > cur_peak_val or math.isnan(cur_peak_val):
			cur_peak_val = prom
			cur_peak_time = cur_time
	return cur_peak_time

def get_formants(s, vowel_time):
	formant = s.to_formant_burg()
	return [formant.get_value_at_time(i, vowel_time) for i in [1,2,3]]

def my_log(fname, formants):
	word = (fname[fname.find('\\')+1:]).split('.')[0]
	return [word, ''] + formants

folders = ['Talker1','Talker2','Talker3']
for j in folders:
	files = glob.glob(j+'/'+'*.wav')
	results = []
	for i in files:
		s = parselmouth.Sound(i)
		vowel_time = find_peak_prom(s.to_intensity())
		print(i,vowel_time)
		results.append(my_log(i, get_formants(s, vowel_time)))
	df = pd.DataFrame(results, columns = ['Word', 'Vowel', 'F1', 'F2', 'F3'])
	df.to_csv('C:\\Users\\0to9a\\Desktop\\HW4\\'+j+'.csv')

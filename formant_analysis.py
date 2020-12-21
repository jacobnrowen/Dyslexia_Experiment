import parselmouth
import numpy as np
import pandas as pd
import glob

def get_prom(s, start, end):
	return s.extract_part(from_time = start, to_time = end).get_intensity()

def find_peak_prom(s, dur):
	cur_start_time = 0.0
	cur_peak_start = 0.0
	cur_peak_val = get_prom(s,cur_start_time, cur_start_time + 0.01)
	while cur_start_time < dur:
		cur_start_time += 0.01
		prom = get_prom(s,cur_start_time, cur_start_time + 0.01)
		if prom > cur_peak_val:
			cur_peak_val = prom
			cur_peak_start = cur_start_time
	return cur_peak_start			

def get_formants(s, vowel_time):
	formant = s.to_formant_burg()
	return [formant.get_value_at_time(i, vowel_time) for i in [1,2,3]]

def my_log(fname, formants):
	word = fname.split('/')[1].split('.')[0]
	return [word, ''] + formants

folders = ['Talker1','Talker2','Talker3']
for j in folders:
	files = glob.glob(fldr+'/'+'*.wav')
	results = []
	for i in files:
		s = parselmouth.Sound(i)
		vowel_time = find_peak_prom(s,s.end_time)
		results.append(my_log(i, get_formants(s, vowel_time)))
	pd.DataFrame(results, columns = ['Word', 'Vowel', 'F1', 'F2', 'F3']).to_csv(j)

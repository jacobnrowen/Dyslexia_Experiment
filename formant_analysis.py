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

vowels = ['a','æ','eɪ','ɛ','i','ɪ','oʊ','u','ʊ','ʌ']
for v in vowels:
	files = glob.glob('recordings/*_'+v+'_*')
	results = []
	for i in files:
		s = parselmouth.Sound(i)
		vowel_time = find_peak_prom(s.to_intensity())
		results.append([i]+get_formants(s, vowel_time))
	df = pd.DataFrame(results, columns = ['File', 'F1', 'F2', 'F3'])
	df.to_csv('Vowel Formants/'+v+' formants.csv')
	print(v,'done')

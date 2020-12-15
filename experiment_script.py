import winsound
import time
import numpy as np
import pandas as pd
import glob
import random

test_types = [...]
tests_per_typ = ...
data_rows = []

def play_vowls(fname_a, fname_b):
	winsound.PlaySound(fname_a, winsound.SND_FILENAME)
	time.sleep(3)
	winsound.PlaySound(fname_b, winsound.SND_FILENAME)
	time.sleep(1)

def ask_about(data_logger, fname_a, fname_b, test_type, vowl_name, is_same, other_vowl = None):
	print('----------')
	print('Listen to these sounds.')
	play_vowls(fname_a, fname_b)
	print("Were the two vowel sounds the same or different? Type 'same' if they were the same, or 'different' if they were different.")
	answer = ''
	while answer != 'same' and answer != 'different':
		answer = input()
		#Just in case there is a problem and the sound must be replayed:
		if answer=='r':
			play_vowls(fname_a, fname_b)
	if is_same:
		is_correct = answer == 'same'
		data_logger.append( [test_type, vowl_name, 'N/A', is_correct] )
	else:
		is_correct = answer == 'different'
		data_logger.append( [test_type, vowl_name, other_vowl, is_correct] )

for typ in test_types:
	all_sounds = glob.glob(typ+'*')
	all_vowels = { i[len(typ)+1:-6] for i in all_sounds }
	for i in range(tests_per_typ):
		if random.choice([True, False]):
			vowl = random.choice(all_vowels)
			fnames = random.shuffle( glob.glob(typ + '_' + vowl + '_*') )
			ask_about(data_rows, fnames[0], fnames[1], typ, vowl, True)
		else:
			vowels = random.sample(all_vowels, 2)
			fnames = [ random.choice(glob.glob(typ + '_' + v + '_*')) for v in vowels]
			ask_about(data_rows, fnames[0], fnames[1], typ, vowels[0], False, vowels[1])

final_results = pd.DataFrame(data_rows, columns = ['Test Type', 'Vowel', 'Other Vowel', 'Correctness'])
print("Enter name of subject.")
subj = input()
final_results.to_csv(subj)
print(final_results)

#Just in case I need to check anything
safe_close = ""
while safe_close != "close":
	safe_close = input()

import winsound
import time
import numpy as np
import pandas as pd
import glob
import random

test_types = ['BareVowel','SameCons','DiffCons','Words']
tests_per_typ = 25
data_rows = []

def play_vowls(fname_a, fname_b):
	winsound.PlaySound(fname_a, winsound.SND_FILENAME)
	time.sleep(0.5)
	winsound.PlaySound(fname_b, winsound.SND_FILENAME)
	time.sleep(0.25)

def ask_about(data_logger, fname_a, fname_b, test_type, vowl_name, is_same, other_vowl = None):
	print('----------')
	print('Listen to these sounds.')
	play_vowls(fname_a, fname_b)
	print("Were the vowel sounds the same or different? Type 'same' if they were the same, or 'different' if they were different.")
	answer = ''
	while answer != 'same' and answer != 'different':
		answer = input()
		#Just in case there is a problem and the sound must be replayed:
		if answer=='r':
			play_vowls(fname_a, fname_b)
	if is_same:
		is_correct = answer == 'same'
		data_logger.append( [test_type, vowl_name, 'N/A', is_correct, fname_a, fname_b] )
	else:
		is_correct = answer == 'different'
		data_logger.append( [test_type, vowl_name, other_vowl, is_correct, fname_a, fname_b] )
print("This is the start of the experiment. Type OK when you are ready to start.")
while input() != 'OK':
		print('Type OK when ready to proceed.')

for typ in test_types:
	all_sounds = glob.glob('recordings/'+typ+'*')
	all_vowels = list({ i[i.find(typ)+len(typ)+1:i.rfind('_')] for i in all_sounds })
	print('This is the start of a new section of the experiment.')
	for i in range(tests_per_typ):
		if random.choice([True, False]):
			vowl = random.choice(all_vowels)
			fnames = glob.glob('recordings/'+typ + '_' + vowl + '_*')
			random.shuffle(fnames)
			ask_about(data_rows, fnames[0], fnames[1], typ, vowl, True)
		else:
			vowels = random.sample(all_vowels, 2)
			fnames = [ random.choice(glob.glob('recordings/'+typ + '_' + v + '_*')) for v in vowels]
			ask_about(data_rows, fnames[0], fnames[1], typ, vowels[0], False, vowels[1])
	print("This is the end of a section of the experiment. Type OK when ready to proceed.")
	while input() != 'OK':
		print('Type OK when ready to proceed.')

final_results = pd.DataFrame(data_rows, columns = ['Test Type', 'Vowel', 'Other Vowel', 'Correctness', 'File One', 'File Two'])
print("Enter name of subject.")
subj = input()
final_results.to_csv(subj)
print(final_results)

#Just in case I need to check anything
safe_close = ""
while safe_close != "close":
	safe_close = input()

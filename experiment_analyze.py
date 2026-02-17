import csv
from datetime import datetime
import json
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

FORMAT = '%Y-%m-%d %H:%M:%S,%f'

def process_results(inf, outf, chosen=None):
	starts = {}
	ends = {}
	data = {}
	
	def makekey(subject, payload): # A tuple of just enough information from the payload to ensure uniqueness - `list` and `index` should be enough (or just `name` on its own, if we assume I didn't make any mistakes in arranging the lists), but we include `system` as well just to be sure
		return subject, payload['system'], payload['list'], payload['index']
	
	with open(inf, 'r', newline='') as f:
		reader = csv.reader(f)
		for line in tqdm(reader):
			stamp, subject, action, payload = line
			payload = json.loads(payload)
			stamp = datetime.strptime(stamp, FORMAT)
		#	stamp = datetime.fromisoformat(stamp)
			if action == 'STIMULUS':
				key = makekey(subject, payload)
				starts[key] = stamp
				data[key] = payload
	#			if subject in chosen: print('Start', key)
			elif action == 'RESPONSE':
				key = makekey(subject, payload)
				ends[key] = stamp
				data[key].update(payload)
	#			if subject in chosen: print('End', key)
	
	with open(outf, 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(('Subject', 'Duration', 'System', 'List', 'Index', 'Which', 'Name', 'Result', 'Accuracy'))
		
		for key in tqdm(ends.keys()):
			subject = key[0]
			if chosen is None or subject in chosen:
				duration = (ends[key] - starts[key]).total_seconds()
				payload = data[key]
				
				row = (
					subject,
					duration,
					payload['system'],
					payload['list'],
					payload['index'],
					payload['which'],
					payload['name'],
					payload['result'],
				)
				
				writer.writerow(row)

def process_surveys(inf, outf, filter=None):
	qs_init = {
		'current':'Currently enrolled in Hittite',
		'semesters':'Semesters taken (including current)',
		'outside':'Outside experience',
		'cv':'Familiarity with V, CV, VC',
		'cvc':'Familiarity with CVC',
		'logo':'Familiarity with logograms',
		'hzl':'Familiarity with the Zeichenlexikon',
		'hantatallas':'Familiarity with Hantatallas',
		'sanhatallas':'Familiarity with Sanhatallas',
		'german':'Can read German',
		'other':'Other information',
	}
	qs_final = {
		'difficulty':'Difficult to use',
		'tiring':'Tiring to use',
		'certainty':'Certain of answers',
		'easiest':'Easiest aspects',
		'worst':'Worst aspects',
		'improve':'Suggested improvements',
		'other':'Other information',
	}
	
	data = defaultdict(dict)
	
	with open(inf, 'r', newline='') as f:
		reader = csv.reader(f)
		for line in tqdm(reader):
			stamp, subject, action, payload = line
			payload = json.loads(payload)
			if filter and subject not in filter: continue
			
			if action == 'SURVEY':
				if payload['which'] == 'initial':
					key = 'I'
				elif payload['which'] == 'final':
					key = payload['system'] # H, Z, S
				else:
					raise ValueError(subject, payload)
				
				data[subject][key] = payload
	
	with open(outf, 'w', newline='') as f:
		writer = csv.writer(f)
		
		row = ['Subject']
		row.extend(qs_init[k] for k in qs_init) # Not using .values for symmetry
		row.extend('H '+qs_final[k] for k in qs_final)
		row.extend('S '+qs_final[k] for k in qs_final)
		row.extend('Z '+qs_final[k] for k in qs_final)
		writer.writerow(row)
		
		for subject, vals in data.items():
			row = [subject]
			row.extend(vals['I'][k] if k in vals['I'] else '' for k in qs_init) # Since early surveys didn't have the sanhatallas question
			row.extend((vals['H'][k] if 'H' in vals else '') for k in qs_final)
			row.extend((vals['S'][k] if 'S' in vals else '') for k in qs_final)
			row.extend((vals['Z'][k] if 'Z' in vals else '') for k in qs_final)
			writer.writerow(row)

def rewrite_for_r():
	data = []
	currently = {}
	semesters = {}
	
	yesno = {'yes' : 1, 'no' : 0}
	
	# First, we read the within-subjects data from surveys.csv
	with Path('surveys.csv').open('r', newline='') as f:
		read = csv.DictReader(f)
		for line in read:
			subj = line['Subject']
			curr = yesno[line['Currently enrolled in Hittite'].lower()] # This will throw an exception on a bad value, which is exactly what we want
			sems = float(line['Semesters taken (including current)']) # Similarly
			if subj in currently: raise ValueError('Subject already exists!', subj)
			
			currently[subj] = curr
			semesters[subj] = sems
	
	# Then, we read each subject's task results from tagged/*.csv
	for fn in tqdm(list(Path('tagged').glob('*.csv'))):
		with fn.open('r', newline='') as f:
			read = csv.DictReader(f)
			for line in tqdm(list(read)):
				if line['List'].startswith('S'): continue # Skip practice data
				data.append({
					'subject'	: line['Subject'],
					'time'		: float(line['Duration']),
					'system'	: line['System'],
					'task'		: line['Name'],
					'accurate'	: int(line['Accuracy']),
					'damage':	 int(line['Name'][0]),
					'enrolled'	: currently[line['Subject']],
					'semesters'	: semesters[line['Subject']],
					'list'		: line['List'],
				})
	
	# And output our finished datatable
	with Path('data_for_r.csv').open('w', newline='') as f:
		write = csv.DictWriter(f, ['subject', 'time', 'system', 'task', 'accurate', 'damage', 'enrolled', 'semesters', 'list'])
		write.writeheader()
		write.writerows(data)

# Subjects removed for inaccuracy: TODO - handled in R
# Subjects removed for other reasons: TODO - handled in R
# Subjects removed for IRB reasons: AY3, CY3, BX3
if __name__ == '__main__':
#	process_surveys('experiment.21.log', 'surveys.csv', {'PAE','PBE','PA1','PB1','PA2','PB2', 'AX1','AX2','AX3','AY1','AY2','BX1','BX2','BY1','BY2','BY3','CX1','CX2','CX3','CY1','CY2'})
	rewrite_for_r()
#	for subj in tqdm(['AX3', 'BY3', 'CX3'], disable=True):
#		print(subj)
#		process_results('experiment.21.log', f'{subj}.csv', [subj])
#	process_surveys('experiment.13.log', 'surveys.csv', {'PAE','PBE','PA1','PB1','PA2','PB2', 'AX1', 'AY1', 'BX1', 'BY1', 'CY1'})

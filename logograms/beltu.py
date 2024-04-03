# Beltu = Akkadian form of GAŠAN because that's what this is made for
# This theme naming really isn't working at this point...oh well

import pickle
import re

MATCH = r'GAŠAN'

def find_matches():
	with open('glyphs.pickle', 'rb') as f:
		tablets = pickle.load(f)
	print(MATCH)
	for ident, glyphs in sorted(tablets.items()):
		if any(re.search(MATCH, glyph) for glyph in glyphs):
			print(f'{ident[0]} {ident[1]}.{ident[2]}')

if __name__ == '__main__':
	find_matches()

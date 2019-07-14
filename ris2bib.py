#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import unidecode

def main(argv = sys.argv):

	argc = len(argv)
	if (argc == 1):
		print "Usage is ris2bib.py [FILE] [-v]"
	else:
		try:
			ris = open(argv[1],'r+')
		except:
			print "Error: No such file."
			return
		
		if (argc == 3 and argv[2] == '-v'):
			verbose = True
		else:
			verbose = False

		entries = r2b_read(ris, verbose)

		ris.close()

		bib_filename = argv[1][:-4]+'.bib' # strip and replace extension
		open(bib_filename,'w+') # strip and replace extension

		for entrie in entries:
			r2b_write(entrie, bib_filename)

def r2b_read(ris, verbose):

	"""
	Reads in a .ris file and returns a .bib format 'entries' dictionary with the appropriate information.
	"""
	entries = dict()
	entries['authors']=list() # Allows for multiple authors
	entries['keywords']=list() 
	values = []	
	for line in ris:

		if re.match("DB",line):
			entries['source'] = line[6:-1].rstrip()
		elif re.match("AN",line):
			entries['id'] = line[6:-1].rstrip().replace(" ", "")
		elif re.match("T1",line):
			entries['title'] = line[6:-1].rstrip().replace('"', '\\"')				
		elif re.match("AU",line):
			entries['authors'].append(line[6:-1].rstrip()) # minus one to remove newline
		elif re.match("KW",line):
			entries['keywords'].append(line[6:-1].rstrip()) # minus one to remove newline			
		elif re.match("PB",line):
			entries['publisher'] = line[6:-1].rstrip()
		elif re.match("AB",line):
			entries['abstract'] = line[6:-1].rstrip().replace('"', '\\"')
		elif re.match("SN",line):
			entries['issn'] = line[6:-1].rstrip()
		elif re.match("SP",line):
			entries['page'] = line[6:-1].rstrip()
		elif re.match("VL",line):
			entries['volume'] = line[6:-1].rstrip()
		elif re.match("IS",line):
			entries['issue'] = line[6:-1].rstrip()
		elif re.match("DO",line):
			entries['doi'] = "https://doi.org/" + line[6:-1].rstrip()
		elif re.match("Y1",line):
			y = line[6:-1].split("/")
			entries['year'] = line[6:-1].rstrip()
			if y:
				entries['year'] = y[0].rstrip()				
		elif re.match("J1",line):
			entries['journal'] = line[6:-1].rstrip()
		elif re.match("UR",line):
			entries['url'] = line[6:-1].rstrip()
		elif re.match("ER",line):
			values.append(entries)
			entries = dict()
			entries['authors']=list() # Allows for multiple authors
			entries['keywords']=list() 
			print 'Unparsed line: ' + line[:-1]
	
	return values
		
def r2b_write(entries,bib_filename):

	"""
	Writes the .bib formatted dictionary to file using .bib file syntax.
	"""

	bib = open(bib_filename,'a') # strip and replace extension

	key = entries['id']
	if 'source' in entries:	
		key = key + str(entries['year']) + ","
		
	if len(entries['authors']) >= 1:
		key = entries['authors'][0][:entries['authors'][0].index(',')] + str(entries['year']) + ","
		#convert plain text to utf-8
		key = unicode(key, "utf-8")
		#convert utf-8 to normal text
		key = unidecode.unidecode(key)
		
	key = key.replace(" ", "").replace("-","")
	bib.write('@ARTICLE{' +  key) # get surname of first author slicing to ','
	if 'source' in entries:		
		bib.write('\n\tsource=\t\"'+ str(entries['source']) + "\",")
	if 'id' in entries:		
		bib.write("\n\tid=\t\"" + str(entries['id']) + "\",")
	if 'title' in entries:	
		bib.write("\n\ttitle=\t\"" + entries['title'].replace('"', "").replace("'","") + "\",")
	if len(entries['authors']) >= 1:
		bib.write('\n\tauthor=\t\"'+entries['authors'][0])
		for entry in entries['authors'][1:]:
			bib.write(" and " + entry)
		bib.write("\",")
	if 'abstract' in entries:
		bib.write("\n\tabstract=\t\"" + entries['abstract'].replace('"', "").replace("'","") + "\",")
	if len(entries['keywords']) >= 1:
		bib.write('\n\tkeywords=\t\"'+entries['keywords'][0].replace('"', "").replace("'",""))
		for entry in entries['keywords'][1:]:
			bib.write(" , " + entry.replace('"', "").replace("'",""))
		bib.write("\",")
	if 'publisher' in entries:		
		bib.write("\n\tpublisher=\t\"" + entries['publisher'].replace('"', "").replace("'","") + "\",")
	if 'year' in entries:
		bib.write('\n\tyear=\t\"'+ entries['year'] + "\",")
	if 'issn' in entries:		
		bib.write('\n\tissn=\t\"'+ entries['issn'] + "\",")
	if 'page' in entries:		
		bib.write('\n\tpage=\t\"'+ entries['page'] + "\",")
	if 'volume' in entries:			
		bib.write("\n\tvolume=\t\"" + entries['volume'] + "\",")
	if 'issue' in entries:
		bib.write("\n\tissue=\t\"" + entries['issue'] + "\",")
	if 'doi' in entries:			
		bib.write("\n\tdoi=\t\"" + entries['doi'] + "\",")
	if 'year' in entries:			
		bib.write("\n\tyear=\t\"" + entries['year'] + "\",")
	if 'journal' in entries:			
		bib.write("\n\tjournal=\t\"" + entries['journal'].replace('"', "").replace("'","") + "\",")
	if 'url' in entries:				
		bib.write("\n\turl=\t\"" + entries['url'] + "\",")
	bib.write("\n}\n")
	bib.close()			

if __name__ == '__main__':
	main()	

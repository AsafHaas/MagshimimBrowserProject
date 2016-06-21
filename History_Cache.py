"""
History Cache Module
----------------
This module will manage the history cache.
The raw history cache is stored in a text file, in the form of:

URL<split_str>Timestamp<breakline>

where each line is a new record.
example: www.domain.com&&01.01.1970\n
(for splitstr='&&')

The parsed history cache is represented in a list of dictionaries,
each cell of the list (a dictionary) being a record.
The dictonary representing a cache record has 2 keys: 
['URL' and 'Time']
"""

import Protocol as ptcl

def write_to_cache(record):
	"""
	This function writes a single record to the history cache
	
	Input:
		record-A dictionary representing a cache record (URL, Time)
	Output:
		None!
	"""
	
	# "a" - Appending a record at the end
	cache = open(ptcl.HISTORY_CACHE_FILE_NAME, "a")
	
	# Forming the record
	line = record["URL"] + ptcl.HISTORY_CACHE_SPLIT_CHAR + \
	record["Time"] + "\n"
	
	cache.write(line)
	
	cache.close()

def get_all_records():
	# r - Reading only
	cache = open(ptcl.HISTORY_CACHE_FILE_NAME, "r")
	records = cache.readlines()
	cache.close()
	
	return parse_raw_records(records)

def read_from_cache(URL):
	"""
	This function reads a single record from the history-cache by key
	of URL
	
	Input:
		URL - A string representing a URL in the cache
	Output:
		A record dictionary if the record exists, and None else
	"""
	
	records = get_all_records()
	
	# Poping out only the records with the matching URL (should be 1)
	ans = [record for record in records if record["URL"] == URL]
	
	# first answer is as good as any (there shouldn't be more than 1)
	return ans[0] if len(ans) > 0 else None
	
def remove_records(URL):
	records = get_all_records()
	
	stays_records = [record for record in records if record["URL"] != URL]
	
	write_full_cache(stays_records)
	
def write_full_cache(records):
	cache = open(ptcl.HISTORY_CACHE_FILE_NAME, "w")
	
	for record in records:
		# Forming the record
		line = record["URL"] + ptcl.HISTORY_CACHE_SPLIT_CHAR + \
		record["Time"] + "\n"
		
		cache.write(line)
		
	cache.close()

def parse_raw_records(raw_records):
	"""
	This function parses the raw cache-data into the data-structure of
	history cache (details above in module doc)
	
	Input:
		raw_records - A list of strings, each one is a raw cache-record
	Output:
		A list of dictionaries with all the records
	"""
	
	# rstrip takes the \n of the last property
	return [{'URL': record.split(ptcl.HISTORY_CACHE_SPLIT_CHAR)[0].rstrip(),\
			'Time': record.split(ptcl.HISTORY_CACHE_SPLIT_CHAR)[1].rstrip()}
						for record in raw_records]

def clear_cache():
	"""
	This function clears the cache from records
	
	Input:
		None!
	Output:
		None!
	"""
	
	# Opening in write mode in order to override the data
	new_cache = open(ptcl.HISTORY_CACHE_FILE_NAME, 'w')
	new_cache.close()

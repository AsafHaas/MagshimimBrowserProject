"""
DNS_Cache Module
----------------
This module will manage the DNS-cache.
The raw DNS-cache is stored in a text file, in the form of:

URL<split_str>IP<split_str>Timestamp<breakline>

where each line is a new record.
example: www.domain.com&&1.1.1.1&&01.01.1970\n
(for splitstr='&&')

The parsed DNS-cache is represented in a list of dictionaries,
each cell of the list (a dictionary) being a record.
The dictonary representing a cache record has 3 keys: 
['URL', 'IP' and 'Time']
"""

import Protocol as ptcl

def write_to_cache(record):
	"""
	This function writes a single record to the DNS cache
	
	Input:
		record-A dictionary representing a cache record (URL, IP, Time)
	Output:
		None!
	"""
	
	# "a" - Appending a record at the end
	cache = open(ptcl.DNS_CACHE_FILE_NAME, "a")
	
	# Forming the record
	line = record["URL"] + ptcl.DNS_CACHE_SPLIT_CHAR + record["IP"] + \
			ptcl.DNS_CACHE_SPLIT_CHAR + record["Time"] + "\n"
	
	cache.write(line)
	
	cache.close()

def read_from_cache(URL):
	"""
	This function reads a single record from the dns-cache by ket of URL
	
	Input:
		URL - A string representing a URL in the cache
	Output:
		A record dictionary if the record exists, and None else
	"""
	
	# r - Reading only
	cache = open(ptcl.DNS_CACHE_FILE_NAME, "r")
	records = cache.readlines()
	cache.close()
	
	records_dicts = parse_raw_records(records)
	
	# Poping out only the records with the matching URL (should be 1)
	ans = [record for record in records_dicts if record["URL"] == URL]
	
	# first answer is as good as any (there shouldn't be more than 1)
	return ans[0] if len(ans) > 0 else None
	

def parse_raw_records(raw_records):
	"""
	This function parses the raw cache-data into the data-structure of
	DNS cache (details above in module doc)
	
	Input:
		raw_records - A list of strings, each one is a raw cache-record
	Output:
		A list of dictionaries with all the records
	"""
	
	# rstrip takes the \n of the last property
	return [{'URL': record.split(ptcl.DNS_CACHE_SPLIT_CHAR)[0].rstrip(),\
			'IP': record.split(ptcl.DNS_CACHE_SPLIT_CHAR)[1].rstrip(),\
			'Time': record.split(ptcl.DNS_CACHE_SPLIT_CHAR)[2].rstrip()}
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
	new_cache = open(ptcl.DNS_CACHE_FILE_NAME, 'w')
	new_cache.close()

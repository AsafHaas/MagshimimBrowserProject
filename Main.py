from scapy.all import *
import datetime
import DNS_Cache as dnscache
import History_Cache as histcache
import Protocol as ptcl

HIST_MENU_SHOW = 1
HIST_MENU_CLEAR = 2
HIST_MENU_DELETE_RECORD = 3

def ARP_req(IP):
	# Returns the MAC address of a given IP address
	
	# First creating arp request:
	request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=IP)
	
	# Sending arp request
	ans, unans=srp(request, timeout=2)
	
	# Checking we got something
	if (len(ans) > 0):
		# We want the first answer in the list, with 2 packets:
		# rquest and response. We want the response, which is index 1
		return ans[0][1][ARP].hwsrc
	else:
		print "Couldn't find MAC of", IP

def DNS_req(domain):
	# Returns the IP address of a given domain
	
	# Forming the DNS query to the dns server, over port 53 UDP with recursion desired so
	# the work will be done for us by the root DNS server
	dns_query = IP(dst=ptcl.DNS_SERVER)/UDP(dport=53)/\
				DNS(rd=1, qd=DNSQR(qname=domain))
				
	ans = sr1(dns_query)
	
	# Checking if there wasn't an answer (status code 3 is name-error)
	if ans[DNS].rcode == 3:
		return None
	
	ip_ans = None
	
	# We get a lot of "answers" in the DNS response (for each dns server in the way),
	# and we want an IP one, so iterating until one matches an IP regex
	i = 0
	
	while not ip_ans:
		curr_ans = ans[DNS][DNSRR][i].rdata
		if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",curr_ans):
			ip_ans = curr_ans
		
		i = i + 1
	
	# Inserting the request to dns cache (assuming it's not there already because if it was
	# we would have retrieve it from there and won't make a request)
	cache_rcrd = {'URL': domain, 'IP': ip_ans, 'Time': str(datetime.datetime.now()) }
	dnscache.write_to_cache(cache_rcrd)
	
	return ip_ans

def Ret_From_Cache(URL):
	# Returns an ip for a URL from the dns_cache, and 0 if the URL isn't
	# in the cache
	
	record = dnscache.read_from_cache(URL)
	
	if record:
		print "YAY: ", URL
		return record["IP"]
	return 0
	
def Find_IP(URL):
	"""
	Return the IP of the URL (Domain Name) passed as argument
	"""
	return Ret_From_Cache(URL) or DNS_req(URL)
	
def generate_ISN():
	"""
	Return a random number to be used as the first sequence number in a TCP connection by the browser's side
	"""
	return random.random(ptcl.MIN_SEQ, ptcl.MAX_SEQ)
	
def Make_GET(URL):
	"""
	Create and send an HTTP GET to the server in the URL passed as argument
	"""
	site_ip = Find_IP(URL)
	host = URL.split("/").pop()
	
	syn_pack = IP(dst=site_ip)/TCP(dport=80, flags="S", \
				seq=generate_ISN())
	
	syn_ack_pack = sr1(syn_pack)
	ack_pack = IP(dst=site_ip)/TCP(dport=80, flags="A", \
			seq=syn_ack_pack[TCP].ack, ack=syn_ack_pack[TCP].seq + 1)
	
	send(ack_pack)

def Update_History(URL):
	"""
	Add the URL passed as argument to the History cache, along with a timestamp
	"""
	record = {"URL": URL, "Time": str(datetime.datetime.now())}
	
	histcache.write_to_cache(record)

def Remove_From_History(URL):
	"""
	Removes all instances of URL passed as argument from the History cache
	"""
	histcache.remove_records(URL)

def show_history():
	"""
	Show all History cache records
	"""
	records = histcache.get_all_records()
	
	if (len(records) > 0):
		for record in records:
			print record["URL"].ljust(ptcl.COLUMN_WIDTH) +\
				ptcl.TABLE_SEP + record["Time"].ljust(ptcl.COLUMN_WIDTH)
	else:
		print "Empty History!"

def hist_menu():
	"""
	Return The history menu to print to the user
	"""
	return """
	History Menu:
	-------------
	%d - Show History
	%d - Clear History
	%d - Remove specific record
	""" % (HIST_MENU_SHOW, HIST_MENU_CLEAR, HIST_MENU_DELETE_RECORD)

def History_Menu():
	"""
	Print to user the history menu, get his choice and act according to it
	"""
	print hist_menu()
	choice = input("Please insert your choice: ")
	
	if choice == HIST_MENU_SHOW:
		show_history()
	elif choice == HIST_MENU_CLEAR:
		Flush_History()
	elif choice == HIST_MENU_DELETE_RECORD:
		record_url = raw_input("Insert URL to remove: ")
		Remove_From_History(record_url)
		print "Done!"
	else:
		print "No such command!"

def Flush_dns():
	"""
	Clear all records from the DNS cache
	"""
	dnscache.clear_cache()

def Flush_History():
	"""
	Clear all records from the History cache
	"""
	histcache.clear_cache()

# History_Menu()
print Find_IP("www.google.com")
print Find_IP("erez.the-class.co.il")

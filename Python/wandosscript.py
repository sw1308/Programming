import os

hostname = raw_input('Enter a domain to ping: ')

for i in xrange(0,10):
	response = os.system('ping -c 100 ' + hostname)
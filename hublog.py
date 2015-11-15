import requests
from BeautifulSoup import BeautifulSoup
import re
import time

# Simple script to grab the downstream table from the web interface for a Virgin Media Super Hub
# and log against date/time.
#
# The script grabs the table then resets the counters, useful for creating a cronjab to collate
# states on error rates, SnR etc.
#
# HTML is passed from function to function to minimise the number of calls made to the router.

ROUTER_ADDR = '192.168.0.1:80'

def reset_all(html):
	html = reset_pre_rs(html)
	html = reset_post_rs(html)
	return html

def reset_pre_rs(html):
	return reset(html, 1)

def reset_post_rs(html):
	return reset(html, 2)

def reset(html, cache):
	# if no page supplied, make a request
	if html is None:
		r = requests.get('http://' + ROUTER_ADDR + '/RouterStatus_downstream.html')
		html = r.text

	# extract the token
	soup = BeautifulSoup(html)
	token = soup.findAll('input', {'type': 'hidden', 'id': None})[0]['name']

	# request a reset and return page contents
	r = requests.post('http://' + ROUTER_ADDR + '/cgi-bin/VmRouterStatusDownstreamCfgCgi', data={'VMChangeCache': cache, token: 0})
	return r.text

def write_values_to_file(html, filename):
	if html is None:
		r = requests.get('http://' + ROUTER_ADDR + '/RouterStatus_downstream.html')
		html = r.text

	soup = BeautifulSoup(html)
	with open(filename, 'w') as f:
		f.write(str(soup.find('table')))

	return html

filename = time.strftime('%Y%m%d-%H%M%S') + '.html'
html = write_values_to_file(None, filename)
reset_all(html)

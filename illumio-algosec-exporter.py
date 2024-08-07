#!/usr/bin/env python3

import sys
import os
import argparse
import logging
import time
import csv
import yaml
from illumio import *

parser = argparse.ArgumentParser()
parser.add_argument('--pce-fqdn', help='PCE FQDN name, will also try to read env var PCE_FQDN', default=os.environ.get('PCE_FQDN'))
parser.add_argument('--pce-org', help='PCE Org Id, will also try to read env var PCE_ORG', default=os.environ.get('PCE_ORG'), type=int)
parser.add_argument('--pce-port', help='PCE Port, will also try to read env var PCE_PORT', default=os.environ.get('PCE_PORT'), type=int)
parser.add_argument('--pce-api-key', help='PCE API Key, will also try to read env var PCE_API_KEY', default=os.environ.get('PCE_API_KEY'))
parser.add_argument('--pce-api-secret', help='PCE API secret, will also try to read env var PCE_API_SECRET', default=os.environ.get('PCE_API_SECRET'))
parser.add_argument('--output-file', help='Output CSV file', default='illumio-algosec-export.csv')
parser.add_argument('--query-file', help='Query file skeleton', default='traffic-config.yaml')
parser.add_argument('--traffic-config', help='Name of the traffic configuration to use', default='default')
parser.add_argument('--algosec-label', '-a', help='Illumio labels to use for the AlgoSec app label, comma separated, e.g. "app", "app,env", "app,env,loc"', default="app")
parser.add_argument('--label-concat', '-c', help='String to use for concatening labels', default="-")
parser.add_argument('--verbose', '-v', help='Verbose output', default=False)

args = parser.parse_args()

if args.verbose:
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
	logging.basicConfig(stream=sys.stdout, level=logging.INFO)


fqdn = args.pce_fqdn
port = args.pce_port
org = args.pce_org
key = args.pce_api_key
secret = args.pce_api_secret
file = args.output_file
query = args.query_file
algosec_labels = args.algosec_label
parsed_labels = algosec_labels.split(",")

logging.debug("Labels: {}".format(parsed_labels))


logging.info("PCE {}, port: {} on org {}, API User: {}".format(fqdn, port, org, key))

# Source IP	Source Name	Destination IP	Destination Name	Service	Service Name	Application Name
header = ['Source IP', 'Source Name', 'Destination IP', 'Destination Name', 'Service','Service Name','Application Name']

# Load the YAML file
with open(query, 'r') as queryfile:
	config = yaml.safe_load(queryfile)

pce = PolicyComputeEngine(fqdn, port=port, org_id=org) 
pce.set_credentials(key, secret)

if pce.check_connection():
	logging.info("Connection to PCE successful.")
else:
	logging.info("Connection to PCE failed. Exiting.")
	exit(1)

### several cache dicts for labels to avoid multiple API calls
label_href_map = {}
value_href_map = {}
label_cache = {}

# building label maps
for l in pce.labels.get():
	label_cache[l.href] = l
	label_href_map[l.href] = {"key": l.key, "value": l.value}
	value_href_map["{}={}".format(l.key, l.value)] = l.href

if args.traffic_config:
	query_config = config['traffic_configs'][args.traffic_config]
else:
	query_config = config['traffic_configs']['default']

### check dates, they must be in the config file
query_start  = query_config.pop('start_date')
query_end  = query_config.pop('end_date')

include_sources = []
if 'include_sources' in query_config:
	sources = query_config.pop('include_sources')
	for s in sources:
		include_sources.append(value_href_map[s])

include_destinations = []
if 'include_destinations' in query_config:
	destinations = query_config.pop('include_destinations')
	for s in destinations:
		include_destinations.append(value_href_map[s])

exclude_sources = []
if 'exclude_sources' in query_config:
	sources_exclude = query_config.pop('exclude_sources')
	for s in sources_exclude:
		exclude_sources.append(value_href_map[s])

exclude_destinations = []
if 'exclude_destinations' in query_config:
	destinations_exclude = query_config.pop('exclude_destinations')
	for s in destinations_exclude:
		exclude_destinations.append(value_href_map[s])

traffic_query = TrafficQuery.build(
	query_start,
	query_end,
	include_sources=include_sources,
	include_destinations=include_destinations,
	exclude_sources=exclude_sources,
	exclude_destinations=exclude_destinations,
	policy_decisions=query_config['policy_decisions']
)

result = pce.get_traffic_flows_async(
	query_name = 'daily_traffic',
	traffic_query = traffic_query
)


logging.debug("Result".format(result))
logging.info("Number of records retrieved from PCE: {}".format(len(result)))

with open(file, "w", encoding = 'UTF-8') as f:
	writer = csv.writer(f)
	writer.writerow(header)
	for flow in result:
		fsrc = flow.src
		fdest = flow.dst

		src = fsrc.ip
		dst = fdest.ip
		service_name = ''
		app = ''
		
		src_name = src
		dst_name = dst

		if fsrc.workload:
			src_name = fsrc.workload.hostname
			if fsrc.workload.hostname:
				src_name = fsrc.workload.hostname
			
		if fdest.workload:
			dst_name = fdest.workload.hostname
			if fdest.workload.hostname:
				dst_name = fdest.workload.hostname

		applist = []

		if fdest.workload != None and fdest.workload.labels != None:
			labels = [ label_cache[x.href] for x in fdest.workload.labels if x.href in label_cache ]
			label_dict = dict(map(lambda x: (x.key, x.value), labels))
			# logging.debug("Labels: {}".format(label_dict))
			for label in parsed_labels:
				logging.debug("Label: {}".format(label))
				if label in label_dict:
					applist.append(label_dict[label])
				else:
					applist.append("Unknown")
			app = args.label_concat.join(applist)

		if flow.service:
			port = flow.service.port
			proto = flow.service.proto

			if proto == 6:
				proto = 'tcp'
			if proto == 17:
				proto = 'udp'
			if proto == 1:
				proto = 'icmp'

			service = "{}/{}".format(proto, port)

		if dst_name == '' or src_name == '':
			continue
	
	
		logging.debug("Src: {}, Src hostname: {}, Dst: {}, Dst hostname: {}, Service: {}, Service name: {}, App Name: {}".format(src,src_name, dst, dst_name, service, service_name, app))
		writer.writerow([src,src_name,dst,dst_name,service,service_name,app])
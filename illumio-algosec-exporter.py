#!/usr/bin/env python3

import requests
import json
import sys
import os
import argparse
import logging
import time
import csv


parser = argparse.ArgumentParser()
parser.add_argument('--pce-fqdn', help='PCE FQDN name, will also try to read env var PCE_FQDN', default=os.environ.get('PCE_FQDN'))
parser.add_argument('--pce-org', help='PCE Org Id, will also try to read env var PCE_ORG', default=os.environ.get('PCE_ORG'))
parser.add_argument('--pce-api-key', help='PCE API Key, will also try to read env var PCE_API_KEY', default=os.environ.get('PCE_API_KEY'))
parser.add_argument('--pce-api-secret', help='PCE API secret, will also try to read env var PCE_API_SECRET', default=os.environ.get('PCE_API_SECRET'))
parser.add_argument('--output-file', help='Output CSV file', default='illumio-algosec-export.csv')
parser.add_argument('--query-file', help='Query file skeleton', default='traffic-query.json')
parser.add_argument('--verbose', '-v', help='Verbose output', default=False)

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)


fqdn = args.pce_fqdn
org = args.pce_org
key = args.pce_api_key
secret = args.pce_api_secret
file = args.output_file
query = args.query_file

logging.info("PCE {} on org {}, API User: {}".format(fqdn, org, key))


# Source IP	Source Name	Destination IP	Destination Name	Service	Service Name	Application Name
header = ['Source IP', 'Source Name', 'Destination IP', 'Destination Name', 'Service','Service Name','Application Name']

# read file
with open(query, 'r') as queryfile:
    data=queryfile.read()

query_data = json.loads(data)

logging.debug("Query: {}".format(query_data))

response = requests.post("{}/api/v2/orgs/{}/traffic_flows/traffic_analysis_queries".format(fqdn, org), auth=(key,secret), data=json.dumps(query_data), headers={"Content-Type": "application/json"})

logging.info("Response: {}".format(response))
result = response.json()

logging.debug("Result".format(result))
logging.info("Number of records retrieved from PCE: {}".format(len(result)))

with open(file, "w", encoding = 'UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for tl in result:
        logging.debug("TL: {}".format(tl))
        src = tl['src']['ip']
        dst = tl['dst']['ip']
        src_name = ''
        dst_name = ''
        service = ''
        service_name = ''
        app = 'Unknown'
        label_dict = {}
    
        if 'workload' in tl['src']:
            if 'workload' in tl['src']['workload']:
                src_name = tl['src']['workload']['hostname']
            else:
                src_name = tl['src']['ip']
        else:
            src_name = tl['src']['ip']

        if 'workload' in tl['dst']:
            if 'workload' in tl['dst']['workload']:
                dst_name = tl['dst']['workload']['hostname']
            else:
                dst_name = tl['dst']['ip']
        else:
            dst_name = tl['dst']['ip']

        if 'workload' in tl['dst'] and 'labels' in tl['dst']['workload']:
            label_dict = dict(map(lambda x: (x['key'], x['value']), tl['dst']['workload']['labels']))
            logging.debug("Labels: {}".format(label_dict))
            if 'app' in label_dict:
                app = label_dict['app']
    
        if 'service' in tl:
            port = tl['service']['port']
            proto = tl['service']['proto']
    
            if proto == 6:
                proto = 'tcp'
            if proto == 17:
                proto = 'udp'
            if proto == 1:
                proto = 'icmp'
    
            service = "{}/{}".format(proto, port)

        if dst_name == '' or src_name == '':
            continue
    
    
        # print("Src: {}, Src hostname: {}, Dst: {}, Dst hostname: {}, Service: {}, Service name: {}, App Name: {}".format(src,src_name, dst, dst_name, service, service_name, app))
        writer.writerow([src,src_name,dst,dst_name,service,service_name,app])
    

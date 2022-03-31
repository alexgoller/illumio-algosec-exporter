# illumio-algosec-exporter

Export Illumio Explorer traffic to AlgoSec AppViz

# Usage

    usage: illumio-algosec-exporter.py [-h] [--pce-fqdn PCE_FQDN] [--pce-org PCE_ORG] [--pce-api-key PCE_API_KEY] [--pce-api-secret PCE_API_SECRET] [--output-file OUTPUT_FILE] [--query-file QUERY_FILE]
    
    optional arguments:
      -h, --help            show this help message and exit
      --pce-fqdn PCE_FQDN   PCE FQDN
      --pce-org PCE_ORG     PCE Org Id
      --pce-api-key PCE_API_KEY
                            PCE API Key
      --pce-api-secret PCE_API_SECRET
                            PCE API secret
      --output-file OUTPUT_FILE
                            PCE API secret
      --query-file QUERY_FILE
                            Query file skeleton

# Traffic query file

A json file is provided that contains a traffic query as documented in https://docs.illumio.com/core/21.5/API-Reference/index.html#Illumio-Core-traffic_flows_async_queries
# Environment vars

If you do not use the command line switches, be sure to have the following
env vars set

* PCE_FQDN - URL for the PCE
* PCE_ORG - your org, defaults to 1
* PCE_API_KEY - your API key, including api_
* PCE_API_SECRET - your API key secret

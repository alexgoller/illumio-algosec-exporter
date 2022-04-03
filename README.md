# illumio-algosec-exporter

Export Illumio Explorer traffic to AlgoSec AppViz

# Usage

usage: illumio-algosec-exporter.py [-h] [--pce-fqdn PCE_FQDN] [--pce-org PCE_ORG] [--pce-api-key PCE_API_KEY] [--pce-api-secret PCE_API_SECRET]
                                   [--output-file OUTPUT_FILE] [--query-file QUERY_FILE] [--algosec-label ALGOSEC_LABEL]
                                   [--label-concat LABEL_CONCAT] [--verbose VERBOSE]

optional arguments:
  -h, --help            show this help message and exit
  --pce-fqdn PCE_FQDN   PCE FQDN name, will also try to read env var PCE_FQDN
  --pce-org PCE_ORG     PCE Org Id, will also try to read env var PCE_ORG
  --pce-api-key PCE_API_KEY
                        PCE API Key, will also try to read env var PCE_API_KEY
  --pce-api-secret PCE_API_SECRET
                        PCE API secret, will also try to read env var PCE_API_SECRET
  --output-file OUTPUT_FILE
                        Output CSV file
  --query-file QUERY_FILE
                        Query file skeleton
  --algosec-label ALGOSEC_LABEL, -a ALGOSEC_LABEL
                        Illumio labels to use for the AlgoSec app label, comma separated, e.g. "app", "app,env", "app,env,loc"
  --label-concat LABEL_CONCAT, -c LABEL_CONCAT
                        String to use for concatening labels
  --verbose VERBOSE, -v VERBOSE
                        Verbose output


# Traffic query file

A json file is provided that contains a traffic query as documented in https://docs.illumio.com/core/21.5/API-Reference/index.html#Illumio-Core-traffic_flows_async_queries
# Environment vars

If you do not use the command line switches, be sure to have the following
env vars set

* PCE_FQDN - URL for the PCE
* PCE_ORG - your org, defaults to 1
* PCE_API_KEY - your API key, including api_
* PCE_API_SECRET - your API key secret

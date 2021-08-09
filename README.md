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

# Environment vars

If you do not use the command line switches, be sure to have the following
env vars set

* PCE_FQDN
* PCE_ORG
* PCE_API_KEY
* PCE_API_SECRET

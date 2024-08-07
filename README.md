# Illumio AlgoSec Exporter

## Description

The Illumio AlgoSec Exporter is a Python-based tool designed to query traffic flow data from an Illumio Policy Compute Engine (PCE) and export it to a CSV file. This tool is particularly useful for organizations using both Illumio and AlgoSec, as it formats the data in a way that can be easily imported into AlgoSec for further analysis.

## Features

- Connects to Illumio PCE using API credentials
- Queries traffic flow data based on configurable parameters
- Exports traffic flow data to a CSV file with customizable headers
- Supports custom label mapping for AlgoSec application names
- Implements efficient label caching to improve performance

## Prerequisites

- Python 3.x
- Access to an Illumio PCE with API credentials
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone this repository or download the script.
2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Set up your PCE connection details either as environment variables or pass them as command-line arguments.
2. Prepare a YAML configuration file (`traffic-query.json` by default) with your desired traffic query parameters.

## Usage

Run the script with the following command:

```
python illumio-algosec-exporter.py [options]
```

### Command-line Options

- `--pce-fqdn`: PCE FQDN name (can also be set via PCE_FQDN environment variable)
- `--pce-org`: PCE Org ID (can also be set via PCE_ORG environment variable)
- `--pce-port`: PCE Port (can also be set via PCE_PORT environment variable)
- `--pce-api-key`: PCE API Key (can also be set via PCE_API_KEY environment variable)
- `--pce-api-secret`: PCE API Secret (can also be set via PCE_API_SECRET environment variable)
- `--output-file`: Output CSV file name (default: 'illumio-algosec-export.csv')
- `--query-file`: Query file skeleton (default: 'traffic-query.json')
- `--algosec-label`: Illumio labels to use for the AlgoSec app label (default: "app")
- `--label-concat`: String to use for concatenating labels (default: "-")
- `--verbose`: Enable verbose output

## Output

The script generates a CSV file with the following headers:

- Source IP
- Source Name
- Destination IP
- Destination Name
- Service
- Service Name
- Application Name

## Example

```
python illumio-algosec-exporter.py --pce-fqdn my.pce.com --pce-org 1 --pce-port 8443 --output-file my_export.csv --algosec-label "app,env"
```

## Notes

- Ensure your PCE API credentials have the necessary permissions to query traffic flow data.
- The tool implements label caching to improve performance. If labels change frequently in your environment, you may need to modify the caching mechanism.

## Troubleshooting

- If you encounter connection issues, verify your PCE credentials and network connectivity.
- For detailed logging, use the `--verbose` flag.

## Contributing

Contributions to improve the Illumio AlgoSec Exporter are welcome. Please submit pull requests or open issues on the project's repository.

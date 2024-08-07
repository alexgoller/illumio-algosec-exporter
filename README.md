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

# Traffic Configuration File

## Overview

The traffic configuration file is a YAML file used by the Illumio AlgoSec Exporter to define parameters for querying traffic flow data from the Illumio Policy Compute Engine (PCE). This file allows you to specify multiple configurations, each with its own set of parameters.

## File Structure

The file should have a top-level key `traffic_configs`, under which you can define multiple named configurations. Each configuration is a set of key-value pairs defining the query parameters.

```yaml
traffic_configs:
  config_name_1:
    # Configuration parameters
  config_name_2:
    # Another set of configuration parameters
```

## Configuration Parameters

Each configuration can include the following parameters:

- `start_date`: The start date for the traffic query (format: "YYYY-MM-DD")
- `end_date`: The end date for the traffic query (format: "YYYY-MM-DD")
- `include_sources`: List of source labels to include in the query
- `include_destinations`: List of destination labels to include in the query
- `policy_decisions`: List of policy decisions to include (e.g., "allowed", "potentially_blocked")
- `max_results`: Maximum number of results to return

## Example Configuration

Here's an example configuration file with two configurations: "default" and "example":

```yaml
traffic_configs:
  default:
    start_date: "2024-08-01"
    end_date: "2024-08-08"
    include_sources: []
    include_destinations: []
    exclude_destinations: []
    exclude_sources: []
    policy_decisions:
      - allowed
      - potentially_blocked
    max_results: 100000
  example:
    start_date: "2024-08-01"
    end_date: "2024-08-08"
    include_sources:
      - "env=dev"
    include_destinations:
      - "env=prod"
    policy_decisions:
      - allowed
      - potentially_blocked
    max_results: 100000
```

### Explanation

1. `default` configuration:
   - Queries traffic between August 1, 2024, and August 8, 2024.
   - Includes all sources and destinations (empty lists).
   - Includes both allowed and potentially blocked traffic.
   - Limits results to 100,000 entries.

2. `example` configuration:
   - Uses the same date range as the default configuration.
   - Includes only sources with the label "env=dev".
   - Includes only destinations with the label "env=prod".
   - Includes both allowed and potentially blocked traffic.
   - Also limits results to 100,000 entries.

## Usage

To use a specific configuration when running the Illumio AlgoSec Exporter, use the `--traffic-config` command-line option followed by the name of the configuration. For example:

```
python illumio-algosec-exporter.py --traffic-config example
```

If no configuration is specified, the script will use the 'default' configuration.

## Notes

- Dates should be in ISO format (YYYY-MM-DD).
- Leave `include_sources` or `include_destinations` as empty lists `[]` to include all sources or destinations.
- Labels in `include_sources` and `include_destinations` should be in the format "key=value".
- Valid `policy_decisions` are typically "allowed", "potentially_blocked", and "blocked", but may depend on your Illumio setup.
- Adjust `max_results` based on your needs and PCE limitations.

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

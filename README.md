# Readme

## Installation

```bash
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x loadTesting.sh
chmod +x stats.sh
```

## Running
```bash
sh loadTesting.sh # runs the Locust distributed load testing
python test.py # records the start and end time of the run
sh stats.sh # Fetch the metrics from AWS Cloudwatch
python plot.py # Need to create folders according to the file (TODO)
```
# Readme

## Installation

Use [AWS CLI](https://aws.amazon.com/cli/) to setup aws credentials before starting

```bash
pip install virtualenv
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running
create a .env file with the following format
```bash
apiURL=https://exampleURL.com
apiId=exampleAPIId
tableName=example-table-name
time=5 #in minutes
users=10
```

Run the write script to populate the DB 
```bash
python write.py
```

Run the load testing using python
```bash
python main.py
```
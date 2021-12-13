# Readme

## Installation

```bash
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
time=5
users=10
```
Run the load testing using python
```bash
python main.py
```

Run the write data in a similar fashion 
```bash
python write.py
```
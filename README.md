# Readme

## Installation


```bash
pip install virtualenv
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
Use [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to setup aws credentials before starting

```bash
aws configure #you will be asked to enter secret ID and secret key
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
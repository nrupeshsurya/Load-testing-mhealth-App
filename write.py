from datetime import date, timedelta
import random
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

tableName = os.getenv('tableName')

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2021, 1, 1)
end_date = date(2021, 12, 31)
data = []
for single_date in daterange(start_date, end_date):
    entry = {
        "PutRequest": {
            "Item": {
                "date": {"S": single_date.strftime("%Y-%m-%d")},
                "walking": {"N": str(random.randint(3600,4000))},
                "standing": {"N":str(random.randint(5000,6000))},
                "sleeping": {"N":str(random.randint(25200,28800))},
                "distance": {"N":str(round(random.uniform(3.0,5.0),2))},
                "averagePace" : {"N":str(round(random.uniform(4.0,6.0),2))},
                "emgIndex" : {"N":str(round(random.uniform(7.0,9.5),2))},
                "totalProcessed" : {"N": str(0)}
            }
        }
    }
    data.append(entry)

finalData = {
    tableName : data
}


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

client = boto3.client('dynamodb')

for x in batch(finalData[tableName], 25):
    subbatch_dict = {tableName: x}
    response = client.batch_write_item(RequestItems=subbatch_dict)


# client = boto3.client('dynamodb')
# tables = client.list_tables()
# print(tables)
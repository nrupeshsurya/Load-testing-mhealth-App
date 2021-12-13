import os
import subprocess
import sys
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt 
import numpy as np
from dotenv import load_dotenv

load_dotenv()
apiURL = os.getenv('apiURL')
apiId = os.getenv('apiId')
tableName = os.getenv('tableName')
time = os.getenv('time')

fig = plt.figure(figsize=(8,11))
rows = 2
columns = 2

def createDirectory(n):
    cwd = os.getcwd()
    directory = f'{n}/results'
    path = os.path.join(cwd,directory)
    try:
        os.makedirs(path, exist_ok=True)
    except:
        print("Directory '%s' cannot be created" % directory)
        quit()
    
def loadTest(n):
    subprocess.run(f'locust -f responseTime.py --host {apiURL} --users {n} --spawn-rate 0.1 --csv={n}/client -t{time}m --headless',shell=True)

def awsStats(n):
    df = pd.read_csv(f'{n}/client_stats_history.csv')
    ts = int(df.iloc[0][0])
    begin = (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:00'))
    ts = int(df.iloc[-1][0])
    close = (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:00'))
    subprocess.run(f"aws cloudwatch get-metric-statistics --namespace AWS/DynamoDB --metric-name SuccessfulRequestLatency --dimensions Name=TableName,Value={tableName} Name=Operation,Value=GetItem --statistics Average --start-time {begin} --end-time {close} --period 60  --region ap-south-1 | jq -r '.Datapoints[] | [.Timestamp, .Average, .Unit] | @csv' > {n}/GetLatency.csv",shell=True)
    subprocess.run(f"aws cloudwatch get-metric-statistics --namespace AWS/DynamoDB --metric-name SuccessfulRequestLatency --dimensions Name=TableName,Value={tableName} Name=Operation,Value=BatchGetItem --statistics Average --start-time {begin} --end-time {close} --period 60  --region ap-south-1 | jq -r '.Datapoints[] | [.Timestamp, .Average, .Unit] | @csv' > {n}/BatchGetLatency.csv",shell=True)
    subprocess.run(f"aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Duration --dimensions Name=FunctionName,Value=processed-data-endpoint-india --statistics Average --start-time {begin} --end-time {close} --period 60  --region ap-south-1 | jq -r '.Datapoints[] | [.Timestamp, .Average, .Unit] | @csv' > {n}/LambdaDuration.csv", shell=True)
    subprocess.run(f"aws cloudwatch get-metric-statistics --namespace AWS/ApiGateway --metric-name Latency --dimensions Name=Stage,Value=\$default Name=ApiId,Value={apiId} --statistics Average --start-time {begin} --end-time {close} --period 60  --region ap-south-1 | jq -r '.Datapoints[] | [.Timestamp, .Average, .Unit] | @csv' > {n}/ApiLatency.csv",shell=True)
    subprocess.run(f"aws cloudwatch get-metric-statistics --namespace AWS/ApiGateway --metric-name IntegrationLatency --dimensions Name=Stage,Value=\$default Name=ApiId,Value={apiId} --statistics Average --start-time {begin} --end-time {close} --period 60  --region ap-south-1 | jq -r '.Datapoints[] | [.Timestamp, .Average, .Unit] | @csv' > {n}/IntegrationLatency.csv",shell=True)
    subprocess.run(f"aws cloudwatch get-metric-statistics --namespace AWS/DynamoDB --metric-name ConsumedReadCapacityUnits --dimensions Name=TableName,Value={tableName} --statistics Sum --start-time {begin} --end-time {close} --period 60  --region ap-south-1 | jq -r '.Datapoints[] | [.Timestamp, .Average, .Unit] | @csv' > {n}/Consumed.csv",shell=True)
    subprocess.run(f"aws cloudwatch get-metric-statistics --namespace AWS/DynamoDB --metric-name ProvisionedReadCapacityUnits --dimensions Name=TableName,Value={tableName} --statistics Average --start-time {begin} --end-time {close} --period 60  --region ap-south-1 | jq -r '.Datapoints[] | [.Timestamp, .Average, .Unit] | @csv' > {n}/Provisioned.csv",shell=True)

def awsPlotHelper(n, i, name, filename):
    fig.add_subplot(rows, columns, i)
    service = pd.read_csv(f'{n}/{filename}.csv', names=['Time','Latency','Unit'])
    service['Time'] = service['Time'].apply(lambda x : str(x)[-9:-1])
    service = service.sort_values('Time')
    service.reset_index(inplace=True)
    Q1 = np.percentile(service['Latency'], 25,
                   interpolation = 'midpoint')
    Q3 = np.percentile(service['Latency'], 75,
                    interpolation = 'midpoint')
    IQR = Q3 - Q1
    # print("Old Shape: ", service.shape)

    upper = np.where(service['Latency'] >= (Q3+1.5*IQR))
    # Lower bound
    lower = np.where(service['Latency'] <= (Q1-1.5*IQR))


    # print(upper[0])
    # print(lower[0])
    # print(service)

    service.drop(upper[0], inplace = True)
    service.drop(lower[0], inplace = True)
    
    # print(service)

    # print("New Shape: ", service.shape)
    print(f"{name} mean is {service['Latency'].mean()}")
    with open(f'{n}/values.txt','a') as file1:
        file1.write(f"{name} mean is {service['Latency'].mean()}\n")

    plt.plot(service['Time'],service['Latency'])
    plt.xticks(rotation=90)
    plt.xlabel('Time')
    plt.ylabel('Latency(ms)')
    plt.title(name)

def clientPlotHelper(n):
    df = pd.read_csv(f'{n}/client_stats_history.csv')
    df = df.iloc[1:]
    df['Timestamp'] = df['Timestamp'].apply(lambda x : datetime.utcfromtimestamp(int(x)).strftime('%H:%M:%S'))
    print(f"Average Client Latency is {df['Total Average Response Time'].iloc[-1]}")

    with open(f'{n}/values.txt','a') as file1:
        file1.write(f"Average Client Latency is {df['Total Average Response Time'].iloc[-1]}\n")
    
    plt.plot(df['Timestamp'],df['95%'],label='95 percentile')
    plt.plot(df['Timestamp'],df['Total Average Response Time'],label='Average')
    plt.xticks(rotation=90)
    # plt.xticks([])
    plt.xlabel('Time')
    plt.ylabel('Latency(ms)')
    plt.title(f'Client latency with upto {n} concurrent users')
    plt.legend(loc="upper right")
    plt.savefig(f'{n}/results/client.png',bbox_inches="tight")
    plt.close()

def plot(n):
    awsPlotHelper(n, 1 ,'API Gateway Latency','ApiLatency')
    # plt.xticks([])
    awsPlotHelper(n, 2, 'Lambda execution', 'LambdaDuration')
    # plt.xticks([])
    awsPlotHelper(n, 3, 'GetItem latency', 'GetLatency')
    # plt.xticks([])
    awsPlotHelper(n, 4, 'BatchGetItem latency', 'BatchGetLatency')
    plt.tight_layout()
    # plt.xticks([])
    plt.savefig(f'{n}/results/{n}.png')
    plt.close()
    clientPlotHelper(n)

if __name__ == '__main__':
    print("hello")
    n = int(sys.argv[1])
    print(n)
    createDirectory(n)
    loadTest(n)
    awsStats(n)
    plot(n)


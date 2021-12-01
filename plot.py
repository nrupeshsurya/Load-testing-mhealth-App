from matplotlib import pyplot as plt
import pandas as pd 
count = 100
i=1
fig = plt.figure(figsize=(8, 11))
rows = 2
columns = 2

def func(name, filename):
    global i
    fig.add_subplot(rows, columns, i)
    ApiGateway = pd.read_csv(f'{count}/{filename}.csv', names=['Time','Latency','Unit'])
    ApiGateway['Time'] = ApiGateway['Time'].apply(lambda x : str(x)[-9:-1])
    ApiGateway = ApiGateway.sort_values('Time')
    plt.plot(ApiGateway['Time'],ApiGateway['Latency'])
    plt.xticks(rotation=90)
    plt.xlabel('Time')
    plt.ylabel('Latency(ms)')
    plt.title(name)
    i+=1
    # plt.savefig(f'{count}/results/{filename}.png',bbox_inches="tight")
    # plt.close()

def response():
    df = pd.read_csv(f'{count}/example_stats_history.csv')
    df = df.iloc[1:]
    
    plt.plot(df['Timestamp'],df['95%'],label='95 percentile')
    plt.plot(df['Timestamp'],df['Total Average Response Time'],label='Average')
    # plt.xticks(rotation=90)
    # plt.xticks([])
    plt.xlabel('Time')
    plt.ylabel('Latency(ms)')
    plt.title(f'Client latency with {count} concurrent users')
    plt.legend(loc="upper right")
    plt.savefig(f'{count}/results/client.png',bbox_inches="tight")
    plt.close()

func('API Gateway Latency','ApiLatency')
# plt.xticks([])
func('Lambda execution', 'LambdaDuration')
# plt.xticks([])
func('GetItem latency', 'GetLatency')
# plt.xticks([])
func('BatchGetItem latency', 'BatchGetLatency')
plt.tight_layout()
# plt.xticks([])
plt.savefig(f'{count}/results/{count}.png')
plt.close()
response()

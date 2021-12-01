from locust import HttpUser, task, between
from calendar import monthrange
import random
from datetime import date, timedelta
import locust.stats
locust.stats.CSV_STATS_INTERVAL_SEC = 60


monthKeyListMain = []
dayListMain = []
weekListMain = []


count = 0
start_date = date(2021, 1, 1)
end_date = date(2022, 1, 1)
delta = timedelta(days=1)
while start_date < end_date:
    # print(start_date.strftime("%Y-%m-%d"))
    dayListMain.append({"date": start_date.strftime("%Y-%m-%d")})
    start_date += delta
    count+=1
    if(count==7):
        print(dayListMain)
        # print(weekListMain)
        count=0
        weekListMain.append(dayListMain)
        dayListMain=[]

dayListMain = []

start_date = date(2021, 1, 1)
end_date = date(2022, 1, 1)
delta = timedelta(days=1)
while start_date < end_date:
    # print(start_date.strftime("%Y-%m-%d"))
    dayListMain.append(start_date.strftime("%Y-%m-%d"))
    start_date += delta

for i in range(1,13):
    monthKeyList = [{'date':'{:04d}-{:02d}-{:02d}'.format(2021, i, d)} for d in range(1, monthrange(2021, i)[1] + 1)]
    monthKeyListMain.append(monthKeyList)

# monthKeyList = [{'date':'{:04d}-{:02d}-{:02d}'.format(2021, 10, d)} for d in range(1, monthrange(2021, 10)[1] + 1)]

weekKeyList = [{'date' : '2021-10-04'},{'date' : '2021-10-05'},{'date' : '2021-10-06'},{'date' : '2021-10-07'},{'date' : '2021-10-08'},{'date' : '2021-10-09'},{'date' : '2021-10-10'}]

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(90)
    def daily_page(self):
        self.client.get(url=f"/items/{dayListMain[random.randint(0,364)]}")

    @task(5)
    def weekly_page(self):
        headers = {'content-type': 'application/json'}
        self.client.post(url="/items", json={
            "keys": weekListMain[random.randint(0,51)]
        }, headers=headers)

    @task(5)
    def monthly_page(self):
        headers = {'content-type': 'application/json'}
        self.client.post(url="/items", json={
            "keys": monthKeyListMain[random.randint(0,11)]
        }, headers=headers)
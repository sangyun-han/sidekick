import datetime
import random
import time
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')


for i in range(0, 1000):
    
    value = random.randint(0, 200)
    hostName = "server-%d" % random.randint(1, 5)
    now = datetime.datetime.now()
    pointValues = [{
            "time": now,
            "measurement": "test_metric",
            "fields": {
                "value": value,
            },
            "tags": {
                "hostName": hostName,
                "region" : "kr"
            }
        }]
    client.write_points(pointValues)
    result = client.query('select value from test_metric;')
    print(result)




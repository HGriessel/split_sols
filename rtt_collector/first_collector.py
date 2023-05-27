import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import requests
# export INFLUXDB_TOKEN=<YOUR_TOKEN>
token = os.environ.get("INFLUXDB_TOKEN")
org = "henri_sols"
bucket="tigsstack"

url = "http://127.0.0.1:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)



api_endpoint ="https://alpha-vantage.p.rapidapi.com/query"

querystring = {"symbol":"MSFT","function":"TIME_SERIES_INTRADAY","interval":"5min","output_size":"compact","datatype":"json"}

headers = {
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}


response = requests.get(api_endpoint, headers=headers, params=querystring)
response_time_ms = response.elapsed.total_seconds() * 1000  # Convert to milliseconds
print(response_time_ms)
print(response.code)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

point = (
    Point("api_response_time")
    .tag("api", "example_api")
    .field("response_time_ms", response_time_ms)
    .field("response_endpoint", api_endpoint)
    .field("response_code", response.code)
)
write_api.write(bucket=bucket, org=org, record=point)

write_client.close()


# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())
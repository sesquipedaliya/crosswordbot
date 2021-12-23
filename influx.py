from influxdb import InfluxDBClient
from environment import Env

DEFAULT_INFLUX_HOST = "influxdb.metrics.ops.marathon.la.mesos.factual.com"
DEFAULT_INFLUX_PORT = "8086"
DEFAULT_INFLUX_USERNAME = "root"
DEFAULT_INFLUX_PASSWORD = "root"
DEFAULT_INFLUX_DB = "crossword"
DEFAULT_INFLUX_MEASUREMENT = "completion_time_fs"


class Reporter:

    def __init__(self, enabled=Env.is_production()):
        self.enabled = enabled
        if not self.enabled:
            print('Reporter is disabled')

        self.client = InfluxDBClient(DEFAULT_INFLUX_HOST, DEFAULT_INFLUX_PORT, DEFAULT_INFLUX_USERNAME,
                                     DEFAULT_INFLUX_PASSWORD, DEFAULT_INFLUX_DB)

    def report(self, name, timestamp, time_sec, channel_id):
        if not self.enabled:
            return
        self.client.write_points(time_precision='s',
                                 points=[{
                                     "measurement": DEFAULT_INFLUX_MEASUREMENT,
                                     "tags": {
                                         "user": name,
                                         "version": 3,
                                         "channel_id": channel_id
                                     },
                                     "fields": {
                                         "seconds": time_sec
                                     },
                                     "time": int(float(timestamp))
                                 }])


from core.data.programs_report_count import ProgramReportsCount
from core.ports.programs_report_persist import ProgramReportsCountPersist
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDbProgramReportsCountPersist(ProgramReportsCountPersist):

    def __init__(self, url: str, username: str, password: str, org: str, bucket: str):
        self._client = InfluxDBClient(url=url, username=username, password=password, org=org)
        self._bucket = bucket

    def persist(self, program_reports_count:ProgramReportsCount):
        p = Point("program_reports_count").tag("slug", program_reports_count.slug).field("count", program_reports_count.reports_count)
        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self._bucket, record=p)
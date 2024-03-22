import influxdb_client


class InfluxDBService:
    def __init__(self, url, token, org):
        '''Establish a connection to InfluxDB'''
        self.org = org
        self.client = influxdb_client.InfluxDBClient(
            url=url, token=token, org=self.org)

    def is_active(self):
        '''Ping InfluxDB service to check if it is active'''
        status = self.client.ping()
        return status

    def run_query(self, query_input):
        '''Run the provided flux query string through the InfluxDB client
           and get the results'''
        query_api = self.client.query_api()
        query_result = query_api.query(org=self.org, query=query_input)
        results = []
        for table in query_result:
            for record in table.records:
                item = {}
                for col in record.values.items():
                    col_name, col_value = col
                    item[col_name] = col_value
                results.append(item)
        return results

    def close_connection(self):
        '''Close the connetion to InfluxDB'''
        self.client.close()

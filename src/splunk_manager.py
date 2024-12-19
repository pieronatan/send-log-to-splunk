import json
import os

from urllib3 import PoolManager


class SplunkLogManager:
    def __init__(self, batch_size=50):
        self.splunk_url = os.environ.get('SPLUNK_HEC_URL')
        self.splunk_token = os.environ.get('SPLUNK_HEC_TOKEN')
        self.splunk_index = os.environ.get('SPLUNK_HEC_INDEX')
        self.batch_size = batch_size
        self.http = PoolManager()
        self.event_list = []

    def add_event(self, log, source_type, log_time, log_time_format):
        self.event_list.append({
            'event': f'{log_time} component={source_type} type=INFO data={json.dumps(log)}',
            'index': self.splunk_index,
            'source': "s3",
            'sourcetype': source_type,
            'time': log_time_format
        })

        if len(self.event_list) >= self.batch_size:
            self._send_batch_to_splunk()

    def _send_batch_to_splunk(self):
        payload = ""
        for event in self.event_list:
            payload += json.dumps(event)

        self._send_to_splunk(payload)
        self.event_list.clear()

    def _send_to_splunk(self, payload):
        try:
            headers = {
                'Authorization': f'Splunk {self.splunk_token}',
                'Content-Type': 'application/json'
            }
            response = self.http.request(
                url=self.splunk_url,
                body=payload,
                method='POST',
                headers=headers
            )
            if response.status != 200:
                raise Exception(f"Error sending log to Splunk: {response.data.decode('utf-8')}")
        except Exception as e:
            raise Exception(f"Error sending log batch to Splunk: {str(e)}")

    def flush(self):
        if self.event_list:
            self._send_batch_to_splunk()

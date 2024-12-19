import gzip
import os
from datetime import datetime

from src.s3 import S3Client
from src.utils import split_by_space_with_quotes


class LogProcessor:
    def __init__(self, splunk_manager, logger):
        self.s3_client = S3Client()
        self.splunk_manager = splunk_manager
        self.logger = logger
        self.source_type_prefix = os.environ.get('SOURCE_TYPE_PREFIX')
    def process_file(self, bucket_name, file_key):
        try:
            obj_gz = self.s3_client.get_object(bucket_name, file_key)
            with gzip.GzipFile(fileobj=obj_gz['Body']) as log_file:
                self.logger.info(f"Processing file: {file_key}")
                for line in log_file:
                    line = line.decode('utf-8').strip()
                    if "elasticloadbalancing" in file_key:
                        self._process_elb_log(line, file_key)
                    else:
                        self._process_cf_log(line, file_key)
                self.logger.info(f"Flushing events: {len(self.splunk_manager.event_list)}")
                self.splunk_manager.flush()
        except Exception as e:
            self.logger.error(f"Error processing file {file_key}: {str(e)}")

    def _process_elb_log(self, line, file_key):
        fields = split_by_space_with_quotes(line)
        lb = fields[2].split('/')[1] if len(fields[2].split('/')) > 2 else ''
        source_type = self.source_type_prefix + '_lb-' + lb
        log = self._parse_elb_log(fields)
        log_time = fields[1]
        log_time_format = datetime.strptime(fields[1], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
        self.splunk_manager.add_event(log, source_type, log_time, log_time_format)

    def _process_cf_log(self, line, file_key):
        fields = line.split('\t')
        if len(fields) >= 32 and not fields[0].startswith("#"):
            log = self._parse_cf_log(fields)
            log_time = f"{fields[0]}T{fields[1]}"
            log_time_format = datetime.strptime(log_time, '%Y-%m-%dT%H:%M:%S').timestamp()
            cf_id = os.path.basename(file_key).split('.')[0]
            source_type = self.source_type_prefix + '_cf-' + cf_id
            self.splunk_manager.add_event(log, source_type, log_time, log_time_format)

    def _parse_elb_log(self, fields):
        return {
            'type': fields[0],
            'elb': fields[2],
            'client_port': fields[3],
            'target_port': fields[4],
            'request_processing_time': fields[5],
            'target_processing_time': fields[6],
            'response_processing_time': fields[7],
            'elb_status_code': fields[8],
            'target_status_code': fields[9],
            'received_bytes': fields[10],
            'sent_bytes': fields[11],
            'request': fields[12].strip('"'),
            'user_agent': fields[13].strip('"'),
            'ssl_cipher': fields[14],
            'ssl_protocol': fields[15],
            'target_group_arn': fields[16],
            'trace_id': fields[17].strip('"'),
            'domain_name': fields[18].strip('"'),
            'chosen_cert_arn': fields[19].strip('"'),
            'matched_rule_priority': fields[20],
            'request_creation_time': fields[21],
            'actions_executed': fields[22].strip('"'),
            'redirect_url': fields[23].strip('"'),
            'error_reason': fields[24].strip('"'),
            'target_port_list': fields[25].strip('"'),
            'target_status_code_list': fields[26].strip('"'),
            'classification': fields[27].strip('"'),
            'classification_reason': fields[28].strip('"'),
            'conn_trace_id': fields[29].strip('"')
        }

    def _parse_cf_log(self, fields):
        return {
            'x-edge-location': fields[2],
            'sc-bytes': fields[3],
            'c-ip': fields[4],
            'cs-method': fields[5],
            'cs(Host)': fields[6],
            'cs-uri-stem': fields[7],
            'sc-status': fields[8],
            'cs(Referer)': fields[9],
            'cs(User-Agent)': fields[10],
            'cs-uri-query': fields[11],
            'cs(Cookie)': fields[12],
            'x-edge-result-type': fields[13],
            'x-edge-request-id': fields[14],
            'x-host-header': fields[15],
            'cs-protocol': fields[16],
            'cs-bytes': fields[17],
            'time-taken': fields[18],
            'x-forwarded-for': fields[19],
            'ssl-protocol': fields[20],
            'ssl-cipher': fields[21],
            'x-edge-response-result-type': fields[22],
            'cs-protocol-version': fields[23],
            'fle-status': fields[24],
            'fle-encrypted-fields': fields[25],
            'c-port': fields[26],
            'time-to-first-byte': fields[27],
            'x-edge-detailed-result-type': fields[28],
            'sc-content-type': fields[29],
            'sc-content-len': fields[30],
            'sc-range-start': fields[31],
            'sc-range-end': fields[32]
        }

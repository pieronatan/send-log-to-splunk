import os

from src.log_processor import LogProcessor
from src.logger import configure_logger
from src.s3 import S3Client
from src.splunk_manager import SplunkLogManager

def process_directory():
    s3_client = S3Client()
    logger = configure_logger()
    splunk_manager = SplunkLogManager()
    processor = LogProcessor(splunk_manager, logger)

    bucket_name = os.environ.get('BUCKET_NAME')
    bucket_prefix = os.environ.get('BUCKET_PREFIX')
    log_files = s3_client.list_files(bucket_name, bucket_prefix)
    for log_file in log_files:
        logger.info(f'Reading {log_file} from {bucket_name}')
        processor.process_file(bucket_name, log_file)
        logger.info(f'Finished processing {log_file} from {bucket_name}')


if __name__ == "__main__":
    process_directory()

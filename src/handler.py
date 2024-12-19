from src.logger import configure_logger
from src.splunk_manager import SplunkLogManager
from src.log_processor import LogProcessor


def handler(event, context):
    logger = configure_logger()

    # Inicialização do SplunkLogManager
    splunk_manager = SplunkLogManager()
    processor = LogProcessor(splunk_manager, logger)

    # Processar o evento S3
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    logger.info(f'Reading {file_key} from {bucket_name}')
    processor.process_file(bucket_name, file_key)
    logger.info(f'Finished processing {file_key} from {bucket_name}')

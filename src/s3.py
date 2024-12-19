import boto3


class S3Client:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def get_object(self, bucket_name, file_key):
        return self.s3.get_object(Bucket=bucket_name, Key=file_key)

    def list_files(self, bucket_name, bucket_prefix):
        paginator = self.s3.get_paginator('list_objects_v2')
        files = []
        for page in paginator.paginate(Bucket=bucket_name, Prefix=bucket_prefix):
            if 'Contents' in page:
                for obj in page['Contents']:
                    files.append(obj['Key'])
        return files

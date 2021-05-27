import boto3
import environ
from botocore.exceptions import ClientError

# Initialise environment variables
env = environ.Env()
environ.Env.read_env(env_file='facturdetect_project/.env')


def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3',
        aws_access_key_id=env('AWS_ACCESS_KEY'),
        aws_secret_access_key=env('AWS_SECRET_KEY')
    )
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return False
    return True

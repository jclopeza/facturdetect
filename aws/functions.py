import boto3
import environ
from botocore.exceptions import ClientError
from utilities.coordinates import invoice_number, invoice_period

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


def get_text(text_found, dict_validator):
    text_extracted = None
    if (
        (text_found["Type"] == dict_validator["Type"]) and
        (dict_validator["Min_Width"] < text_found["Geometry"]["BoundingBox"]["Width"] < dict_validator["Max_Width"]) and
        (dict_validator["Min_Height"] < text_found["Geometry"]["BoundingBox"]["Height"] < dict_validator["Max_Height"]) and
        (dict_validator["Min_Left"] < text_found["Geometry"]["BoundingBox"]["Left"] < dict_validator["Max_Left"]) and
        (dict_validator["Min_Top"] < text_found["Geometry"]["BoundingBox"]["Top"] < dict_validator["Max_Top"])
    ):
        text_extracted = text_found["DetectedText"]
    return text_extracted


def detect_text(img_prefix, img_num, bucket):
    rekognition_client = boto3.client('rekognition',
        aws_access_key_id=env('AWS_ACCESS_KEY'),
        aws_secret_access_key=env('AWS_SECRET_KEY')
    )
    # Vamos a analizar tan solo la primera imagen
    photo = f'{img_prefix}-1.jpg'
    response = rekognition_client.detect_text(Image={'S3Object': {'Bucket':bucket, 'Name':photo}})
    textDetections = response['TextDetections']
    # Vamos a crear y devolver un diccionario con el número de factura identificado
    invoice_number_found = False
    invoice_period_found = False
    for text in textDetections:
        if not invoice_number_found:
            invoice_n = get_text(text, invoice_number)
            if invoice_n is not None:
                print("Invoice number: %s" % invoice_n)
                invoice_number_found = True
        if not invoice_period_found:
            invoice_p = get_text(text, invoice_period)
            if invoice_p is not None:
                print("Invoice period: %s" % invoice_p)
                invoice_period_found = True
    values_found = {'numero_factura': invoice_n,
                    'periodo_de_facturacion': invoice_p,
                    'fecha_de_emision': "13-5-2018",
                    'contrato': "23765540",
                    'inicio_contrato': "1-4-2015",
                    'fin_contrato': "4-7-2025"
                    }
    return values_found

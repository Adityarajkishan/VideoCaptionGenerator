import logging
import boto3
from botocore.exceptions import ClientError
import os

'''
# AWS S3 configuration
S3_BUCKET = 'your-s3-bucket-name'
S3_ACCESS_KEY = 'your-access-key'
S3_SECRET_KEY = 'your-secret-key'
S3_REGION = 'your-s3-region'

# Initialize an S3 client
s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY, region_name=S3_REGION)

'''

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return None
    print(response)
    return response


'''
docker container run -it -v /tmp:/tmp -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker/containers:/var/lib/docker/containers:ro -e ACCOUNT_UUID={9ba88b66-c96f-40d6-b4f8-1575328567a1} -e REPOSITORY_UUID={fa169a8c-22c8-4dff-a5ba-22e0012c295e} -e RUNNER_UUID={20497d8f-a455-5303-b959-caa1501f6228} -e RUNTIME_PREREQUISITES_ENABLED=true -e OAUTH_CLIENT_ID=1IZSGvPav1H8KtflEst7fHF6HK80LB7Y -e OAUTH_CLIENT_SECRET=ATOAW7g2930-DRwWkhurTTdM7oFqSQrHdPF1DynTjflLw8o648S2yW2Jba4QriMIT-d0CD4ED34D -e WORKING_DIRECTORY=/tmp --name runner-20497d8f-a455-5303-b959-caa1501f6228 docker-public.packages.atlassian.com/sox/atlassian/bitbucket-pipelines-runner:1
Unable to find image 'docker-public.packages.atlassian.com/sox/atlassian/bitbucket-pipelines-runner:1' locally
1: Pulling from sox/atlassian/bitbucket-pipelines-runner
'''
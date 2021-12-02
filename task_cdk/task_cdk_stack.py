from aws_cdk import (
     core as cdk,
     aws_s3 as s3,
     aws_lambda as lambda_,
     aws_s3_notifications as s3_notify,
)
import os, boto3, logging
from botocore.client import ClientError

class TaskCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #create new s3 bucket and src&dest folders in it
        s3_client = boto3.client('s3')
        s3_resource = boto3.resource('s3')

        def create_bucket(bucket_name, region=None):
            try:
                if region is None:
                    s3_client = boto3.client('s3')
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client = boto3.client('s3', region_name=region)
                    location = {'LocationConstraint': region}
                    s3_client.create_bucket(Bucket=bucket_name,
                                            CreateBucketConfiguration=location)
            except ClientError as e:
                logging.error(e)
                return False
            return True

        bucket_name = 'task-buck'
        region = 'eu-central-1'
        create_bucket(bucket_name, region)
        
        src_dir_name = "task-directory-source"
        dest_dir_name = "task-directory-destination"
        s3_client.put_object(Bucket = bucket_name, Key = (src_dir_name+'/'))
        s3_client.put_object(Bucket = bucket_name, Key = (dest_dir_name+'/'))


#create lambda function
        function = lambda_.Function(self, "TaskLambdaFunction",
                                    runtime = lambda_.Runtime.PYTHON_3_9,
                                    handler = "lambda_handler.main",
                                    code = lambda_.Code.from_asset("./lambda")
        )
        
#send notification to lambda & create notification when object put in bucket
        notification = s3_notify.LambdaDestination(function)
        #bucket.add_event_notification(s3.EventType.OBJECT_CREATED_PUT, notification)

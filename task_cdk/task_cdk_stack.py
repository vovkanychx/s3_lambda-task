from aws_cdk import (
     core as cdk,
     aws_s3 as s3,
     aws_lambda as _lambda,
     aws_s3_notifications as s3_notify,
     aws_iam as iam
)

from aws_cdk.custom_resources import (
    AwsCustomResource, AwsCustomResourcePolicy, PhysicalResourceId
)
import boto3, json

class TaskCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        task_bucket_name = 'task-buck'
        src_dir = 'task-src-dir/'
        dest_dir = 'task-dest-dir/'
        client = boto3.client('s3')
        #new s3 bucket
        s3bucket = s3.Bucket(self, 'TaskBucket',
                            bucket_name = task_bucket_name,
                            auto_delete_objects = True,
                            removal_policy = cdk.RemovalPolicy.DESTROY
                            )     

        #lambda function        
        lambda_function = _lambda.Function(self, 'TaskLambdaFunction',
            code = _lambda.AssetCode('./lambda'),
            handler = 'lambda_handler.main',
            runtime = _lambda.Runtime.PYTHON_3_9
            )

        #lambda trigger        
        s3bucket.add_object_created_notification(
            s3_notify.LambdaDestination(lambda_function),
            s3.NotificationKeyFilter(prefix = "task-src-dir")
        )

        #create directories as put keys
        AwsCustomResource(self, "DirSrc",
            on_create = {
                "service": "S3",
                "action": "putObject",
                "parameters": {'Bucket': task_bucket_name,
                'Key': src_dir
                },
                "physical_resource_id": PhysicalResourceId.of(task_bucket_name)
            },
            policy = AwsCustomResourcePolicy.from_sdk_calls(resources = AwsCustomResourcePolicy.ANY_RESOURCE)
        )
        AwsCustomResource(self, "DirDest",
            on_create = {
                "service": "S3",
                "action": "putObject",
                "parameters": {'Bucket': task_bucket_name,
                'Key': dest_dir
                },
                "physical_resource_id": PhysicalResourceId.of(task_bucket_name)
            },
            policy = AwsCustomResourcePolicy.from_sdk_calls(resources = AwsCustomResourcePolicy.ANY_RESOURCE)
        )

        #add policy to perform actions 
        #(i had errors with put_object, copy_object, head_bucket permissions in event logs, that's to avoid it)
        #cannot put_bucket_policy when deploying for the first time says 'nosuchbucket'
        # copy_policy = {
        #     "Version": "2012-10-17",
        #     "Statement": [
        #         {   
        #             "Principal": "*",
        #             "Effect": "Allow",
        #             "Action": "*",
        #             "Resource": [
        #                 "arn:aws:s3:::task-buck",
        #                 "arn:aws:s3:::task-buck/*"
        #             ]
        #         }
        #     ]
        # }
        # copy_policy = json.dumps(copy_policy)
        # client.put_bucket_policy(Bucket = task_bucket_name, Policy=copy_policy)

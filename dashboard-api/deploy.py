from __future__ import print_function
import os
import sys
import git
import shutil
from time import strftime, sleep
import boto3
import zipfile
from botocore.exceptions import ClientError

REPO_URL = "https://github.com/georgymh/decentralized-ml-js"
REPO_PATH = "/tmp/decentralized-ml-js"
ZIP_PATH = '/tmp/cloud-node.zip'

APPLICATION_NAME = "cloud-node"
S3_BUCKET = "cloud-node-deployment"

VERSION_LABEL = strftime("%Y%m%d%H%M%S")
BUCKET_KEY = APPLICATION_NAME + '/' + VERSION_LABEL + '-cloudnode_builds.zip'


def upload_to_s3(artifact):
    """
    Uploads an artifact to Amazon S3
    """
    try:
        client = boto3.client('s3')
    except ClientError as err:
        print("Failed to create boto3 client.\n" + str(err))
        return False

    try:
        client.put_object(
            Body=open(artifact, 'rb'),
            Bucket=S3_BUCKET,
            Key=BUCKET_KEY
        )
    except ClientError as err:
        print("Failed to upload artifact to S3.\n" + str(err))
        return False
    except IOError as err:
        print("Failed to access artifact.zip in this directory.\n" + str(err))
        return False

    return True

def create_new_version():
    """
    Creates a new application version in AWS Elastic Beanstalk
    """
    try:
        client = boto3.client('elasticbeanstalk')
    except ClientError as err:
        print("Failed to create boto3 client.\n" + str(err))
        return False

    try:
        response = client.create_application_version(
            ApplicationName=APPLICATION_NAME,
            VersionLabel=VERSION_LABEL,
            Description='New build from Bitbucket',
            SourceBundle={
                'S3Bucket': S3_BUCKET,
                'S3Key': BUCKET_KEY
            },
            Process=True
        )
    except ClientError as err:
        print("Failed to create application version.\n" + str(err))
        return False

    try:
        if response['ResponseMetadata']['HTTPStatusCode'] is 200:
            return True
        else:
            print(response)
            return False
    except (KeyError, TypeError) as err:
        print(str(err))
        return False

def deploy_new_version(env_name):
    """
    Deploy a new version to AWS Elastic Beanstalk
    """
    try:
        client = boto3.client('elasticbeanstalk')
    except ClientError as err:
        print("Failed to create boto3 client.\n" + str(err))
        return False

    try:
        response = client.create_environment(
            ApplicationName=APPLICATION_NAME,
            EnvironmentName=env_name,
            VersionLabel=VERSION_LABEL,
            SolutionStackName="64bit Amazon Linux 2018.03 v2.12.11 running Docker 18.06.1-ce",
        )
    except ClientError as err:
        print("Failed to update environment.\n" + str(err))
        return False

    print(response)
    return True


def pre_steps():
    try:
        shutil.rmtree(REPO_PATH)
        shutil.rmtree(ZIP_PATH)
    except:
        pass

def clone_repo():
    git.exec_command('clone', REPO_URL)
    return REPO_PATH

def zip_server_directory():

    shutil.make_archive(ZIP_PATH.split('.zip')[0], 'zip', REPO_PATH + "/server")
    return ZIP_PATH

def deploy_cloud_node(env_name):
    if not upload_to_s3(ZIP_PATH):
        sys.exit(1)
    if not create_new_version():
        sys.exit(1)
    # Wait for the new version to be consistent before deploying
    sleep(5)
    if not deploy_new_version(env_name):
        sys.exit(1)
    return True


def run_deploy_routine(repo_id):
    pre_steps()
    _ = clone_repo()
    _ = zip_server_directory()
    _ = deploy_cloud_node(repo_id)
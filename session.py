import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.session.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
    )

def get_client(region_name):
    return session.client("ec2", region_name=region_name)

def get_resource(region_name):
    return session.resource("ec2", region_name=region_name)

def get_client_elb(region_name):
    return session.client("elb", region_name=region_name)

def get_client_autoscaling(region_name):
    return session.client("autoscaling", region_name=region_name)
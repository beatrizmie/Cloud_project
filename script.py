from keypair import create_key_pair
from instance import create_instance, get_instance_info, terminate_instance
from security_group import create_security_group
from ami import create_image
from load_balancer import create_load_balancer
from auto_scaling import create_launch_configuration, create_auto_scaling_group

# =================================================== VARIABLES ====================================================

# OHIO
ohio_key_name = 'ohioKey'
ohio_region_name = "us-east-2"
ohio_image_id = "ami-0dd9f0e7df0f0a138"
ohio_user_data = """#!/bin/sh
                     sudo apt update
                     cd /home/ubuntu
                     sudo apt install postgresql postgresql-contrib -y
                     sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud';"
                     sudo -u postgres createdb -O cloud tasks
                     sed -i "59 c listen_addresses='*'" /etc/postgresql/10/main/postgresql.conf
                     sed -i "$ a host all all 0.0.0.0/0 trust" /etc/postgresql/10/main/pg_hba.conf
                     sudo ufw allow 5432/tcp
                     sudo systemctl restart postgresql
                     """
ohio_SG_name = 'Ohio SG'
ohio_SG_tag_name = 'Database Security Group'
ohio_ip_permissions = [
    {
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 5432,
        'ToPort': 5432,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
],

# NORTH VIRGINIA
north_virginia_key_name = 'northVirginiaKey'
north_virginia_region_name = "us-east-1"
north_virginia_image_id = "ami-0817d428a6fb68645"
north_virginia_SG_name = 'North Virginia SG'
north_virginia_SG_tag_name = 'ORM Security Group'
north_virginia_ip_permissions = [
    {
        "IpProtocol": "tcp",
        "FromPort": 22,
        "ToPort": 22,
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    },
    {
        "IpProtocol": "tcp",
        "FromPort": 8080,
        "ToPort": 8080,
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    },
    {
        "IpProtocol": "tcp",
        "FromPort": 80,
        "ToPort": 80,
        "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
    },
],

# DATABASE
database_tag_name = 'Database Instance'

# ORM
orm_tag_name = 'ORM Instance'

# AMI
image_name = 'ORM AMI'

# LOAD BALANCER
load_balancer_name = 'LoadBalancer'
LB_tag_name = 'LB'

# AUTO SCALING GROUP
auto_scaling_group_name = 'AutoScaling'
ASG_tag_name = 'ASG'
launch_configuration_name = 'LaunchConfiguration'

# AVAILABILITY ZONES
availability_zones = [
    'us-east-1a',
    'us-east-1b',
    'us-east-1c',
    'us-east-1d',
    'us-east-1e',
    'us-east-1f',
]

# =================================================== SCRIPT ====================================================

# create key pair for ohio
create_key_pair(ohio_key_name, ohio_region_name)

# create security group in ohio
create_security_group(ohio_region_name, ohio_SG_name,
                      ohio_SG_tag_name, ohio_ip_permissions)

# create instance in ohio
create_instance(ohio_key_name, ohio_region_name, ohio_image_id, [
                ohio_SG_name], database_tag_name, ohio_user_data)

# get ohio instance public ip and set user data for north virginia
public_ip = get_instance_info(ohio_region_name, [database_tag_name], 'InstanceIp')
north_virginia_user_data = """#!/bin/sh
                            sudo apt update
                            cd /home/ubuntu
                            git clone https://github.com/beatrizmie/tasks.git
                            sudo sed -i "83 c \\\t'HOST': '{0}'," tasks/portfolio/settings.py
                            cd tasks
                            ./install.sh
                            sudo reboot
                            """.format(public_ip)

# create key pair for north virginia
create_key_pair(north_virginia_key_name, north_virginia_region_name)

# create security group in north virginia
create_security_group(north_virginia_region_name, north_virginia_SG_name,
                      north_virginia_SG_tag_name, north_virginia_ip_permissions)

# create instance in north virginia
create_instance(north_virginia_key_name, north_virginia_region_name, north_virginia_image_id, [
                north_virginia_SG_name], orm_tag_name, north_virginia_user_data)

# create image from north virginia instance
create_image(north_virginia_region_name, orm_tag_name, image_name)

# terminate north virginia instance
terminate_instance(north_virginia_region_name, orm_tag_name)

# create load balancer
create_load_balancer(north_virginia_region_name, [
                     north_virginia_SG_name], load_balancer_name, list(availability_zones), LB_tag_name)

# create launch configuration and auto scaling group
create_launch_configuration(north_virginia_region_name, [image_name], [
                            north_virginia_SG_name], launch_configuration_name, north_virginia_key_name)
create_auto_scaling_group(north_virginia_region_name, auto_scaling_group_name,
                          launch_configuration_name, load_balancer_name, availability_zones, ASG_tag_name)

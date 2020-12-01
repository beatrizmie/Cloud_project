from session import get_client_elb
from security_group import get_security_group_id
from botocore.exceptions import ClientError


def create_load_balancer(regionName, securityGroupName, loadBalancerName, availabilityZones, LBTagName):

    print("\nCreating load balancer...")

    try:
        securityGroupId = get_security_group_id(regionName, securityGroupName)
        load_balancer_response = get_client_elb(regionName).create_load_balancer(
            LoadBalancerName=loadBalancerName,
            Listeners=[
                {
                    'Protocol': 'HTTP',
                    'LoadBalancerPort': 80,
                    'InstancePort': 8080,
                },
            ],
            AvailabilityZones=availabilityZones,
            SecurityGroups=[securityGroupId],
            Tags=[
                {
                    'Key': 'Name',
                    'Value': LBTagName
                },
                {
                    'Key': 'Owner',
                    'Value': 'Beatriz Mie'
                },
            ]
        )

        print("Successfully created %s" % loadBalancerName)

    except ClientError as e:
        print('Error', e)

    return


def delete_load_balancer(regionName, loadBalancerName):

    print("\nDeleting load balancer...")

    try:
        get_client_elb(regionName).delete_load_balancer(
            LoadBalancerName=loadBalancerName)
        print("Successfully deleted %s" % loadBalancerName)

    except ClientError as e:
        print('Error', e)

    return
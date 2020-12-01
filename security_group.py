from session import get_client
from botocore.exceptions import ClientError

def create_security_group(regionName, securityGroupName, SGTagName, ipPermissions):

    client = get_client(regionName)
    vpc_id = client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')

    print("\nCreating Security Group...")

    try:
        security_group_response = client.create_security_group(
            GroupName=securityGroupName,
            Description='Creating Security Group to test Database access',
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key' : 'Name',
                            'Value' : SGTagName
                        },
                        {
                            'Key' : 'Owner',
                            'Value' : 'Beatriz Mie'
                        },
                    ],
                },
            ],
            VpcId=vpc_id
        )
        
        security_group_id = security_group_response['GroupId']
        print('Security Group %s succesfully created in %s.' % (security_group_id, vpc_id))

        data = client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=ipPermissions[0]
        )

        if (data['ResponseMetadata']['HTTPStatusCode'] == 200):
            print('Successfully set ip permissions!')
        else:
            print('Failed to add ip permissions')

    except ClientError as e:
        print(e)

    return


def get_security_group_id(regionName, securityGroupName):

    security_group_id = get_client(regionName).describe_security_groups(
        GroupNames=securityGroupName
    )

    return security_group_id['SecurityGroups'][0]['GroupId']


def delete_security_group(regionName, securityGroupName):

    print("\nDeleting Security Group...")

    try:
        response = get_client(regionName).delete_security_group(GroupName=securityGroupName)
        print('Succesfully deleted %s' % (securityGroupName))

    except ClientError as e:
        print(e)
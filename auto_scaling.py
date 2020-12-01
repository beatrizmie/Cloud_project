from session import get_client, get_client_autoscaling
from ami import get_image_id
from security_group import get_security_group_id
from botocore.exceptions import ClientError

# =================================================== LAUNCH CONFIGURATION ========================================================================

def create_launch_configuration(regionName, imageName, securityGroupName, launchConfigurationName, keyName):

    print('\nCreating launch configuration...')

    try:
        image_id = get_image_id(regionName, imageName)
        securityGroupId = get_security_group_id(regionName, securityGroupName)
        
        launch_config_response = get_client_autoscaling(regionName).create_launch_configuration(
            LaunchConfigurationName=launchConfigurationName,
            ImageId=image_id,
            KeyName=keyName,
            SecurityGroups=[securityGroupId],
            InstanceType='t2.micro',
            InstanceMonitoring={'Enabled': True},
        )

        print("Successfully created %s" % launchConfigurationName)

    except ClientError as e:
        print('Error', e)

    return


def delete_launch_configuration(regionName, launchConfigurationName):

    print("\nDeleting launch configuration...")

    try:
        get_client_autoscaling(regionName).delete_launch_configuration(
            LaunchConfigurationName=launchConfigurationName
        )
        print("Succesfully deleted %s" % launchConfigurationName)

    except ClientError as e:
        print('Error', e)

    return

# =================================================== AUTO SCALING ========================================================================

def create_auto_scaling_group(regionName, autoScalingGroupName, launchConfigurationName, loadBalancerName, availabilityZones, ASGTagName):

    print('\nCreating auto scaling group...')
    client_as = get_client_autoscaling(regionName)

    try:
        auto_scaling_response = client_as.create_auto_scaling_group(
            AutoScalingGroupName=autoScalingGroupName,
            LaunchConfigurationName=launchConfigurationName,
            MinSize=2,
            MaxSize=3,
            LoadBalancerNames=[loadBalancerName],
            DesiredCapacity=2,
            AvailabilityZones=availabilityZones,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': ASGTagName
                },
                {
                    'Key': 'Owner',
                    'Value': 'Beatriz Mie'
                },
            ]
        )

        if (len(get_client_autoscaling(regionName).describe_auto_scaling_groups(AutoScalingGroupNames=[autoScalingGroupName])['AutoScalingGroups']) > 0):
            print("Successfully created %s" % autoScalingGroupName)

        else:
            print("Failed creating auto scaling group")

    except ClientError as e:
        print('Error', e)

    return


def delete_auto_scaling_groups(regionName, autoScalingGroupName):

    print("\nDeleting auto scaling group...")

    try:
        get_client_autoscaling(regionName).delete_auto_scaling_group(
            AutoScalingGroupName=autoScalingGroupName, ForceDelete=True)
        print("Succesfully deleted %s" % autoScalingGroupName)

    except ClientError as e:
        print('Error', e)

    return

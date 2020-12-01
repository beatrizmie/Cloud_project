from session import get_resource, get_client
from botocore.exceptions import ClientError

def create_instance(keyName, regionName, imageId, securityGroupName, instanceTagName, userData):

   client = get_client(regionName)
   print("\nCreating instance...")

   try:
      instance_response = get_resource(regionName).create_instances(
         InstanceType='t2.micro',
         ImageId=imageId,
         KeyName=keyName,
         MinCount=1,
         MaxCount=1,
         SecurityGroups=securityGroupName,
         TagSpecifications=[
            {
               'ResourceType': 'instance',
               'Tags': [
                  {
                     'Key': 'Name',
                     'Value': instanceTagName
                  },
                  {
                     'Key': 'Owner',
                     'Value': 'Beatriz Mie'
                  },
               ],
            },
         ],
         UserData=userData,
      )

      client.get_waiter('instance_status_ok').wait(InstanceIds=[instance_response[0].id])

      if (client.describe_instance_status(InstanceIds=[instance_response[0].id])['InstanceStatuses'][0]['InstanceStatus']['Status'] == 'ok'):
         print("Succesfully created instance %s in %s" % (instance_response[0].id, regionName))

      else:
         print("Failed creating instance :(")

   except ClientError as e:
        print(e)

   return


def get_instance_info(regionName, instanceTagName, instanceInfo):

   try: 
      instance_response = get_client(regionName).describe_instances(
         Filters=[
            {
               'Name': 'tag:Name',
               'Values': instanceTagName
            },
            {
               'Name': 'instance-state-name',
               'Values': ['running']
            },
         ],
      )

      if (len(instance_response['Reservations']) > 0):

         if (instanceInfo == 'InstanceIp'):
            return instance_response['Reservations'][0]['Instances'][0]['PublicIpAddress']
         elif (instanceInfo == 'InstanceId'):
            return instance_response['Reservations'][0]['Instances'][0]['InstanceId']

      else: 
         print("Failed to get %s" % instanceInfo)

   except ClientError as e:
      print('Error', e)

   return


def terminate_instance(regionName, instanceTagName):

   client = get_client(regionName)
   print("\nTerminating instance...")

   try:
      instance_response = client.describe_instances(
         Filters=[
            {
               'Name': 'tag:Name',
               'Values': [instanceTagName]
            },
            {
               'Name': 'instance-state-name',
               'Values': ['running']
            },
         ],
      )

      if (len(instance_response['Reservations']) > 0):

         instanceId = instance_response['Reservations'][0]['Instances'][0]['InstanceId']
         instance = get_resource(regionName).Instance(instanceId)

         response = client.terminate_instances(
            InstanceIds=[
               instanceId,
            ],
         )

         instance.wait_until_terminated()
         print('Succesfully terminated instance %s' % (instanceId))

      else:
         print("There are no instances to terminate!")

   except ClientError as e:
      print('Error', e)

   return
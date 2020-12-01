from session import get_resource, get_client
from instance import get_instance_info
from botocore.exceptions import ClientError

def create_image(regionName, ormTagName, imageName):

    print('\nCreating image...')

    try:
        instance_id = get_instance_info(regionName, [ormTagName], 'InstanceId')

        image_response = get_client(regionName).create_image(InstanceId=instance_id, Name=imageName)
        image = get_resource(regionName).Image(image_response['ImageId'])

        waiter = get_client(regionName).get_waiter('image_available')
        waiter.wait(ImageIds=[image_response["ImageId"]])

        if (image.state == 'available'):
            print("Successfully created %s" % imageName)

    except ClientError as e:
        print('Error', e)
        
    return


def get_image_id(regionName, imageName):

    image_id = get_client(regionName).describe_images(
            Filters=[{
                'Name': 'name',
                'Values': imageName
            }]
        )

    return image_id['Images'][0]['ImageId']


def delete_image(regionName, imageName):

    print("\nDeleting images...")

    try:
        image_response = get_client(regionName).deregister_image(ImageId=get_image_id(regionName, imageName))
        print("Succesfully deleted %s" % imageName)
    
    except ClientError as e:
        print('Error', e)

    return
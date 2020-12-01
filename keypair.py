import os
from session import get_client

def create_key_pair(keyName, regionName):

    print("\nCreating key...")

    try:
        keyPair = get_client(regionName).create_key_pair(KeyName=keyName)
        
        with open("{0}.pem".format(keyName), "w") as file:
            file.write(keyPair['KeyMaterial'])

        print("Succesfully created %s" % (keyName))
    
    except Exception as error:
        print(error)


def delete_key_pair(keyName, regionName):
    
    print("\nDeleting key...")

    try:
        keyPair = get_client(regionName).delete_key_pair(KeyName=keyName)
        os.remove("{0}.pem".format(keyName))

        print("Succesfully deleted %s" % (keyName))

    except Exception as error:
        print(error)
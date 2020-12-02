from keypair import delete_key_pair
from instance import terminate_instance
from security_group import delete_security_group
from ami import delete_image
from load_balancer import delete_load_balancer
from auto_scaling import delete_launch_configuration, delete_auto_scaling_groups

# =================================================== VARIABLES ====================================================

#OHIO
ohio_key_name = 'ohioKey'
ohio_region_name = "us-east-2"
ohio_SG_name = 'Ohio SG'

#NORTH VIRGINIA
north_virginia_key_name = 'northVirginiaKey'
north_virginia_region_name = "us-east-1"
north_virginia_SG_name = 'North Virginia SG'

#DATABASE
database_tag_name = 'Database Instance'

#AMI
image_name = 'ORM AMI'

#LOAD BALANCER
load_balancer_name = 'LoadBalancer'

#AUTO SCALING GROUP
auto_scaling_group_name = 'AutoScaling'
launch_configuration_name = 'LaunchConfiguration'

# =================================================== SCRIPT ====================================================

# delete auto scaling group and launch configuration
delete_auto_scaling_groups(north_virginia_region_name, auto_scaling_group_name)
delete_launch_configuration(north_virginia_region_name, launch_configuration_name)

# delete load balancer
delete_load_balancer(north_virginia_region_name, load_balancer_name)

# delete image
delete_image(north_virginia_region_name, [image_name])

# terminate instance
terminate_instance(ohio_region_name, database_tag_name)

# delete security groups
delete_security_group(north_virginia_region_name, north_virginia_SG_name)
delete_security_group(ohio_region_name, ohio_SG_name)

# delete key pairs
delete_key_pair(north_virginia_key_name, north_virginia_region_name)
delete_key_pair(ohio_key_name, ohio_region_name)

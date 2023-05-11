import boto3

# Create an EC2 client
ec2_client = boto3.client('ec2')

# Output file name
output_file = 'security_group_ports.txt'

# Open the file in write mode
with open(output_file, 'w') as file:
    # Get the list of regions
    regions = ec2_client.describe_regions()['Regions']

    # Iterate over each region
    for region in regions:
        region_name = region['RegionName']
        
        # Create an EC2 resource in the current region
        ec2_resource = boto3.resource('ec2', region_name=region_name)
        
        # Get the list of security groups
        security_groups = ec2_resource.security_groups.all()
        
        # Iterate over each security group
        for security_group in security_groups:
            security_group_id = security_group.id
            
            # Get the inbound rules for the security group
            inbound_rules = security_group.ip_permissions
            
            # Iterate over each inbound rule
            for rule in inbound_rules:
                ip_protocol = rule['IpProtocol']
                from_port = rule['FromPort']
                to_port = rule['ToPort']
                
                # Check if there are specific IP ranges allowed
                if 'IpRanges' in rule:
                    for ip_range in rule['IpRanges']:
                        cidr_ip = ip_range['CidrIp']
                        file.write(f"Region: {region_name}, Security Group ID: {security_group_id}, Opened Port: {from_port}-{to_port}, Rule Type: IP Range, CIDR IP: {cidr_ip}\n")
                
                # Check if there are security groups referenced
                if 'UserIdGroupPairs' in rule:
                    for group_pair in rule['UserIdGroupPairs']:
                        group_id = group_pair['GroupId']
                        file.write(f"Region: {region_name}, Security Group ID: {security_group_id}, Opened Port: {from_port}-{to_port}, Rule Type: Security Group, Referenced Group ID: {group_id}\n")

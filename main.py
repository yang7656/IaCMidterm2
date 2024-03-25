#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws import provider, instance, iam_role, subnet, vpc, iam_instance_profile

import json


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        provider.AwsProvider(self, "AWS", region="us-west-1")
        
        midterm_vpc = vpc.Vpc(
            self,
            "midterm_vpc",
            cidr_block="10.0.0.0/16",
            enable_dns_support=True,
            enable_dns_hostnames=True
        )
        
        midterm_subnet = subnet.Subnet(
            self,
            "midterm_subnet",
            vpc_id=midterm_vpc.id,
            cidr_block="10.0.1.0/24",
            availability_zone="us-west-1b",
        )
        
        midterm_role = iam_role.IamRole(
            self,
            "midterm_role",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Resource": "*"
                }
            })
        )
        
        midterm_instance_profile = iam_instance_profile.IamInstanceProfile(
            self, 
            "InstanceProfile",
            role=midterm_role.name
        )
    
        midterm_instance = instance.Instance(
            self, 
            "midterm",
            ami="ami-01456a894f71116f2",
            instance_type="t2.micro",
            subnet_id=midterm_subnet.id,
            iam_instance_profile=midterm_instance_profile.name,
            user_data="#!/bin/bash\nyum update -y && yum install -y git httpd php && service httpd start && chkconfig httpd on && aws s3 cp s3://seis665-public/index.php /var/www/html/\n",
            tags={
                "Name": "MidtermInstance"
            }
        )



app = App()
MyStack(app, "midtermEC2")

app.synth()

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

# snippet-start:[python.example_code.ec2.Hello]
import boto3


def hello_ec2(ec2_client):
    """
    Use the AWS SDK for Python (Boto3) to create an Amazon Elastic Compute Cloud
    (Amazon EC2) client and list the security groups in your account.
    This example uses the default settings specified in your shared credentials
    and config files.

    :param ec2_client: A Boto3 EC2 Client object. This object is a low-level
                       client that provides a simple programming interface
                       to the underlying EC2 service API.
    """
    print("Hello, Amazon EC2! Let's list up to 10 of your security groups:")
    response = ec2_client.describe_security_groups()
    for sg in response['SecurityGroups'][:10]:
        print(f"\t{sg['GroupId']}: {sg['GroupName']}")


if __name__ == "__main__":
    hello_ec2(boto3.client("ec2"))
# snippet-end:[python.example_code.ec2.Hello]
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

# snippet-start:[python.example_code.ec2.Hello]
def hello_ec2(ec2_client):
    """
    Use the AWS SDK for Python (Boto3) to create an Amazon Elastic Compute Cloud
    (Amazon EC2) client and list the security groups in your account.
    This example uses the default settings specified in your shared credentials
    and config files.

    :param ec2_client: A Boto3 EC2 Client object. This object provides low-level
                       access to the EC2 service API.
    """
    print("Hello, Amazon EC2! Let's list up to 10 of your security groups:")
    try:
        response = ec2_client.describe_security_groups(MaxResults=10)
        for sg in response["SecurityGroups"]:
            print(f"\t{sg['GroupId']}: {sg['GroupName']}")
    except ClientError as err:
        logger.error(
            "Couldn't list security groups. Here's why: %s: %s",
            err.response["Error"]["Code"], err.response["Error"]["Message"]
        )
        raise err


if __name__ == "__main__":
    hello_ec2(boto3.client("ec2"))
# snippet-end:[python.example_code.ec2.Hello]
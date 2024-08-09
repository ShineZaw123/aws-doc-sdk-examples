import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


# snippet-start:[python.example_code.ec2.InstanceWrapper.class]
# snippet-start:[python.example_code.ec2.InstanceWrapper.decl]
class InstanceWrapper:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) instance actions using the client interface."""

    def __init__(self, ec2_client, instance=None):
        """
        :param ec2_client: A Boto3 Amazon EC2 client. This client provides low-level 
                           access to AWS EC2 services.
        :param instance: A Boto3 Instance object. This is a high-level object that
                           wraps instance actions.
        """
        self.ec2_client = ec2_client
        self.instance = instance

    @classmethod
    def from_client(cls):
        ec2_client = boto3.client("ec2")
        return cls(ec2_client)

    # snippet-end:[python.example_code.ec2.InstanceWrapper.decl]

    # snippet-start:[python.example_code.ec2.RunInstances]
    def create(self, image, instance_type, key_pair, security_groups=None):
        """
        Creates a new EC2 instance. The instance starts immediately after
        it is created.

        The instance is created in the default VPC of the current account.

        :param image: The ID of an Amazon Machine Image (AMI) that defines attributes
                      of the instance that is created. The AMI defines things like the 
                      kind of operating system and the type of storage used by the instance.
        :param instance_type: The type of instance to create, such as 't2.micro'.
                              The instance type defines things like the number of CPUs and
                              the amount of memory.
        :param key_pair: The name of the key pair that is used to secure connections
                         to the instance.
        :param security_groups: A list of security group IDs that represent the
                                security groups that are used to grant access to the
                                instance. When no security groups are specified, the
                                default security group of the VPC is used.
        :return: The ID of the newly created instance.
        """
        try:
            instance_params = {
                "ImageId": image,
                "InstanceType": instance_type,
                "KeyName": key_pair,
            }
            if security_groups is not None:
                instance_params["SecurityGroupIds"] = security_groups
            response = self.ec2_client.run_instances(**instance_params, MinCount=1, MaxCount=1)
            self.instance = response["Instances"][0]
            self.ec2_client.get_waiter("instance_running").wait(InstanceIds=[self.instance["InstanceId"]])
            return self.instance["InstanceId"]
        except ClientError as err:
            logging.error(
                "Couldn't create instance with image %s, instance type %s, and key %s. "
                "Here's why: %s: %s",
                image,
                instance_type,
                key_pair,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.RunInstances]

    # snippet-start:[python.example_code.ec2.DescribeInstances]
    def display(self, indent=1):
        """
        Displays information about an instance.

        :param indent: The visual indent to apply to the output.
        """
        if self.instance is None:
            logger.info("No instance to display.")
            return

        try:
            response = self.ec2_client.describe_instances(InstanceIds=[self.instance["InstanceId"]])
            instance = response["Reservations"][0]["Instances"][0]
            ind = "\t" * indent
            print(f"{ind}ID: {instance['InstanceId']}")
            print(f"{ind}Image ID: {instance['ImageId']}")
            print(f"{ind}Instance type: {instance['InstanceType']}")
            print(f"{ind}Key name: {instance['KeyName']}")
            print(f"{ind}VPC ID: {instance['VpcId']}")
            print(f"{ind}Public IP: {instance['PublicIpAddress']}")
            print(f"{ind}State: {instance['State']['Name']}")
        except ClientError as err:
            logger.error(
                "Couldn't display your instance. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.DescribeInstances]

    # snippet-start:[python.example_code.ec2.TerminateInstances]
    def terminate(self):
        """
        Terminates an instance and waits for it to be in a terminated state.
        """
        if self.instance is None:
            logger.info("No instance to terminate.")
            return

        instance_id = self.instance["InstanceId"]
        try:
            self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            self.ec2_client.get_waiter("instance_terminated").wait(InstanceIds=[instance_id])
            self.instance = None
        except ClientError as err:
            logging.error(
                "Couldn't terminate instance %s. Here's why: %s: %s",
                instance_id,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.TerminateInstances]

    # snippet-start:[python.example_code.ec2.StartInstances]
    def start(self):
        """
        Starts an instance and waits for it to be in a running state.

        :return: The response to the start request.
        """
        if self.instance is None:
            logger.info("No instance to start.")
            return

        try:
            response = self.ec2_client.start_instances(InstanceIds=[self.instance["InstanceId"]])
            self.ec2_client.get_waiter("instance_running").wait(InstanceIds=[self.instance["InstanceId"]])
        except ClientError as err:
            logger.error(
                "Couldn't start instance %s. Here's why: %s: %s",
                self.instance["InstanceId"],
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response

    # snippet-end:[python.example_code.ec2.StartInstances]

    # snippet-start:[python.example_code.ec2.StopInstances]
    def stop(self):
        """
        Stops an instance and waits for it to be in a stopped state.

        :return: The response to the stop request.
        """
        if self.instance is None:
            logger.info("No instance to stop.")
            return

        try:
            response = self.ec2_client.stop_instances(InstanceIds=[self.instance["InstanceId"]])
            self.ec2_client.get_waiter("instance_stopped").wait(InstanceIds=[self.instance["InstanceId"]])
        except ClientError as err:
            logger.error(
                "Couldn't stop instance %s. Here's why: %s: %s",
                self.instance["InstanceId"],
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response

    # snippet-end:[python.example_code.ec2.StopInstances]

    # snippet-start:[python.example_code.ec2.DescribeImages]
    def get_images(self, image_ids):
        """
        Gets information about Amazon Machine Images (AMIs) from a list of AMI IDs.

        :param image_ids: The list of AMIs to look up.
        :return: A list of Amazon Machine Image (AMI) information.
        """
        try:
            response = self.ec2_client.describe_images(ImageIds=image_ids)
            return response["Images"]
        except ClientError as err:
            logger.error(
                "Couldn't get images. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.DescribeImages]

    # snippet-start:[python.example_code.ec2.DescribeInstanceTypes]
    def get_instance_types(self, architecture):
        """
        Gets instance types that support the specified architecture and are designated
        as either 'micro' or 'small'. When an instance is created, the instance type
        you specify must support the architecture of the AMI you use.

        :param architecture: The kind of architecture the instance types must support,
                             such as 'x86_64'.
        :return: A list of instance types that support the specified architecture
                 and are either 'micro' or 'small'.
        """
        try:
            response = self.ec2_client.describe_instance_types(
                Filters=[
                    {
                        "Name": "processor-info.supported-architecture",
                        "Values": [architecture],
                    },
                    {"Name": "instance-type", "Values": ["*.micro", "*.small"]},
                ]
            )
            return [it["InstanceType"] for it in response["InstanceTypes"]]
        except ClientError as err:
            logger.error(
                "Couldn't get instance types. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    # snippet-end:[python.example_code.ec2.DescribeInstanceTypes]


# snippet-end:[python.example_code.ec2.InstanceWrapper.class]
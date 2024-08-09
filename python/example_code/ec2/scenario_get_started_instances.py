import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# snippet-start:[python.example_code.ec2.Scenario_GetStartedInstances]
class Ec2InstanceScenario:
    """Runs an interactive scenario that shows how to get started using EC2 instances."""

    def __init__(self, ec2_client, ssm_client):
        """
        :param ec2_client: A Boto3 Amazon EC2 client.
        :param ssm_client: A Boto3 AWS Systems Manager client.
        """
        self.ec2_client = ec2_client
        self.ssm_client = ssm_client

    @demo_func
    def create_and_list_key_pairs(self):
        """
        1. Creates an RSA key pair and saves its private key data as a .pem file in secure
           temporary storage. The private key data is deleted after the example completes.
        2. Lists the first five key pairs for the current account.
        """
        key_wrapper = KeyPairWrapper(self.ec2_client)
        key_name = q.ask("Enter a unique name for your key: ", q.non_empty)
        key_wrapper.create(key_name)
        # Rest of the function implementation remains the same

    @demo_func
    def create_security_group(self):
        """
        1. Creates a security group for the default VPC.
        2. Adds an inbound rule to allow SSH. The SSH rule allows only
           inbound traffic from the current computer's public IPv4 address.
        3. Displays information about the security group.
        """
        sg_wrapper = SecurityGroupWrapper(self.ec2_client)
        sg_name = q.ask("Enter a unique name for your security group: ", q.non_empty)
        security_group = sg_wrapper.create(
            sg_name, "Security group for example: get started with instances."
        )
        # Rest of the function implementation remains the same

    @demo_func
    def create_instance(self):
        """
        1. Gets a list of Amazon Linux 2 AMIs from AWS Systems Manager. Specifying the
           '/aws/service/ami-amazon-linux-latest' path returns only the latest AMIs.
        2. Gets and displays information about the available AMIs and lets you select one.
        3. Gets a list of instance types that are compatible with the selected AMI and
           lets you select one.
        4. Creates an instance with the previously created key pair and security group,
           and the selected AMI and instance type.
        5. Waits for the instance to be running and then displays its information.
        """
        inst_wrapper = InstanceWrapper(self.ec2_client)
        key_wrapper = KeyPairWrapper(self.ec2_client)
        sg_wrapper = SecurityGroupWrapper(self.ec2_client)
        # Rest of the function implementation remains the same

    @demo_func
    def associate_elastic_ip(self):
        """
        1. Allocates an Elastic IP address and associates it with the instance.
        2. Displays an SSH connection string that uses the Elastic IP address.
        """
        eip_wrapper = ElasticIpWrapper(self.ec2_client)
        inst_wrapper = InstanceWrapper(self.ec2_client)
        # Rest of the function implementation remains the same

    @demo_func
    def stop_and_start_instance(self):
        """
        1. Stops the instance and waits for it to stop.
        2. Starts the instance and waits for it to start.
        3. Displays information about the instance.
        4. Displays an SSH connection string. When an Elastic IP address is associated
           with the instance, the IP address stays consistent when the instance stops
           and starts.
        """
        inst_wrapper = InstanceWrapper(self.ec2_client)
        eip_wrapper = ElasticIpWrapper(self.ec2_client)
        # Rest of the function implementation remains the same

    @demo_func
    def cleanup(self):
        """
        1. Disassociate and delete the previously created Elastic IP.
        2. Terminate the previously created instance.
        3. Delete the previously created security group.
        4. Delete the previously created key pair.
        """
        eip_wrapper = ElasticIpWrapper(self.ec2_client)
        inst_wrapper = InstanceWrapper(self.ec2_client)
        sg_wrapper = SecurityGroupWrapper(self.ec2_client)
        key_wrapper = KeyPairWrapper(self.ec2_client)
        # Rest of the function implementation remains the same

    def run_scenario(self):
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

        print("-" * 88)
        print(
            "Welcome to the Amazon Elastic Compute Cloud (Amazon EC2) get started with instances demo."
        )
        print("-" * 88)

        self.create_and_list_key_pairs()
        self.create_security_group()
        self.create_instance()
        self.stop_and_start_instance()
        self.associate_elastic_ip()
        self.stop_and_start_instance()
        self.cleanup()

        print("\nThanks for watching!")
        print("-" * 88)


if __name__ == "__main__":
    try:
        scenario = Ec2InstanceScenario(
            boto3.client("ec2"),
            boto3.client("ssm"),
        )
        scenario.run_scenario()
    except Exception:
        logging.exception("Something went wrong with the demo.")
# snippet-end:[python.example_code.ec2.Scenario_GetStartedInstances]
import boto3
import mysql.connector
from mysql.connector.constants import ClientFlag

## Enable IAM AUTH by running the command
## > ALTER USER 'admin' IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS';

# RDS settings (these should come from environment variables or a configuration file)
rds_host = 'host'
rds_port = 3306
db_user = 'user'
db_name = 'db'
region = 'region'

# Create an RDS client
rds_client = boto3.client('rds', region_name=region)

def get_iam_token():
    """
    Generate an IAM authentication token for connecting to the RDS instance.
    """
    token = rds_client.generate_db_auth_token(
        DBHostname=rds_host,
        Port=rds_port,
        DBUsername=db_user,
        Region=region
    )
    return token

def connect_to_rds():
    """
    Connect to the RDS instance using IAM authentication.
    """
    iam_token = get_iam_token()

    ssl_config = {
        ## To download https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html#UsingWithRDS.SSL.CertificatesDownload
        'ssl_ca': 'us-east-1-bundle.pem'
    }

    try:
        # Create a connection to the RDS instance
        connection = mysql.connector.connect(
            host=rds_host,
            port=rds_port,
            user=db_user,
            password=iam_token,
            # database=db_name,
            ssl_ca=ssl_config['ssl_ca'],
            client_flags=[ClientFlag.SSL],
            auth_plugin='mysql_clear_password'
        )

        print("Connected to RDS MySQL instance")

        # Run a sample query
        cursor = connection.cursor()
        cursor.execute("show databases")
        result = cursor.fetchall()
        print("Query result:", result)

        # Close the connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    connect_to_rds()


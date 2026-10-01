import boto3
import json

def get_database_credentials():
    client = boto3.client(
        "secretsmanager",
        region_name="us-east-1"
    )

    response = client.get_secret_value(
        SecretId="prod/myapp/rds-database"
    )

    secret = json.loads(response["SecretString"])

    return secret

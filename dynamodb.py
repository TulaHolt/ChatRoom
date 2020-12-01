"""
Create dynamodb table
"""
import boto3
# Get the service resource.
import key_config as keys

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=keys.ACCESS_KEY_ID,
                          aws_secret_access_key=keys.ACCESS_SECRET_KEY, region_name="us-east-1")


# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='userdata',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        }

    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='userdata')

# Print out some data about the table.
print(table.item_count)




"""
Create dynamodb table

Used to make a new Dynamodb table. To achieve this just run this file
"""
import boto3

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")


# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='room',
    KeySchema=[
        {
            'AttributeName': 'roomname',
            'KeyType': 'HASH'
        }

    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'roomname',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='room')

# Print out some data about the table.
print(table.item_count)




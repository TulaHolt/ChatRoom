from .Model import Model
from datetime import datetime
import boto3

class model(Model):
    def __init__(self):
        self.resource = boto3.resource("dynamodb", region_name="us-east-1")
        self.table = self.resource.Table('hiking_final')
        try:
            self.table.load()
        except:
            self.resource.create_table(
                TableName="hiking_final",
                KeySchema=[
                    {
                        "AttributeName": "name",
                        "KeyType": "HASH"
                    }
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "name",
                        "AttributeType": "S"
                    }
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1
                }
            )

    def select(self):
        try:
            gbentries = self.table.scan()
        except Exception as e:
            return([['scan failed', '.', '.', '.']])

        return([ [f['name'], f['streetaddress'], f['city'], f['state'], f['zipcode'], f['date'], f['note']] for f in gbentries['Items']])

    def insert(self,name,streetaddress, city, state, zipcode, date, note):
        gbitem = {
            'name' : name,
	    'streetaddress' : streetaddress, 
	    'city' : city, 
	    'state' : state, 
	    'zipcode' : zipcode, 
	    'date' : date,
	    'note' : note,
            }

        try:
            self.table.put_item(Item=gbitem)
        except:
            return False

        return True

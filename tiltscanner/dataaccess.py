from __future__ import print_function # Python 2/3 compatibility
import os
os.environ["TZ"] = "UTC"
import boto3
import json
import fermentationutils
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

def initialize_tables():

    initialize_fermentation()
    initialize_fermentation_detail()

def initialize_fermentation():
    
    table = dynamodb.create_table(
        TableName='Fermentation',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'start_date',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'start_date',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

def initialize_fermentation_detail():
    
    table = dynamodb.create_table(
        TableName='Fermentation_Detail',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'sample_date',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'sample_date',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

def create_fermentation(fermentation_name, original_gravity):

    table = dynamodb.Table('Fermentation')

    name = fermentation_name
    start_date = datetime.now()

    response = table.put_item(
        Item={
            'name':name,
            'start_date':str(start_date),
            'original_gravity':original_gravity
            }
        )

def create_fermentation_event(fermentation_name, original_gravity, specific_gravity, temperature,
                              device_id, mac_address):
    
    table = dynamodb.Table('Fermentation_Detail')

    name = fermentation_name
    sample_date = datetime.now()

    response = table.put_item(
        Item={
            'name':name,
            'sample_date':str(sample_date),
            'original_gravity':original_gravity,
            'specific_gravity':specific_gravity,
            'abv':str(fermentationutils.calculate_abv(original_gravity, specific_gravity)),
            'temperature':temperature,
            'device_id':device_id,
            'mac_address':mac_address
            }
        )






































        
    
    

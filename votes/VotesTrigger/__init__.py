import json
import logging
import os
import uuid
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from datetime import datetime


def main(msg: func.QueueMessage) -> None:
    body = msg.get_body().decode('utf-8')
    body_json = json.loads(body)
    table_service = TableService(connection_string=os.environ["TableStorage"])

    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

    task = Entity()
    task.PartitionKey = body_json["party"]
    task.RowKey = str(uuid.uuid4())
    task.count = body_json["count"]
    task.electoralPlace = body_json["electoralPlace"]
    task.electoralUnit = body_json["electoralUnit"]

    table_service.insert_entity('votes', task)

    # datetime object containing current date and time
    now = datetime.now()
    logging.info(now.strftime("%d/%m/%Y %H:%M:%S") + ' - Processing done')

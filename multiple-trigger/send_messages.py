import os
import sys
import time
from azure.storage.queue import (QueueClient, TextBase64EncodePolicy,
                                 TextBase64DecodePolicy)


try:
    connection_string = os.environ['AzureWebJobsStorage']
    queue_name_1 = "in-hellokeda-multiple-1"
    queue_name_2 = "in-hellokeda-multiple-2"
except KeyError:
    print('Error: missing environment variable AzureWebJobsStorage or QUEUE_NAME')
    exit(1)

queue1 = QueueClient.from_connection_string(
    conn_str=connection_string, queue_name=queue_name_1, message_encode_policy=TextBase64EncodePolicy())
queue2 = QueueClient.from_connection_string(
    conn_str=connection_string, queue_name=queue_name_2, message_encode_policy=TextBase64EncodePolicy())

for message in range(0, int(sys.argv[1])):
    queue1.send_message('foo_queue_1_'+str(message))
    queue2.send_message('foo_queue_2_'+str(message))

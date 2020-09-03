import os
import sys
import json
from random import randrange
from azure.storage.queue import (QueueClient, TextBase64EncodePolicy)


try:
    connection_string = os.environ['QUEUE_STORAGE']
    queue_name = os.environ['QUEUE_NAME']

    parties = ['it'.upper(), 'csharp'.upper(), 'java'.upper(), 'python'.upper()]
    regions = ['A', 'B', 'C', 'D']
    places = ['Sarajevo', 'Zenica', 'Banja Luka', 'Pale']

    queue = QueueClient.from_connection_string(conn_str=connection_string, queue_name=queue_name,
                                               message_encode_policy=TextBase64EncodePolicy())

    for count in range(0, int(sys.argv[1])):
        msg_body = {
            "party": parties[randrange(0, 3)],
            "count": randrange(1, 25),
            "electoralPlace": places[randrange(0, 3)],
            "electoralUnit": regions[randrange(0, 3)]
        }

        queue.send_message(json.dumps(msg_body))

except KeyError:
    print('Error: missing environment variable QUEUE_STORAGE or QUEUE_NAME, or something went wrong')
    exit(1)

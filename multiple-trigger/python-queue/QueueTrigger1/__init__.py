import logging

import azure.functions as func


def main(msg: func.QueueMessage) -> None:
    logging.info('Python 1 queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

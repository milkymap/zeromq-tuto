

import zmq 

import click 

from src.log import logger 

from time import sleep 
from uuid import uuid4

from typing import List 


@click.command()
@click.option('--endpoint')
def handler(endpoint:str):
    ctx = zmq.Context()
    req_socket:zmq.Socket = ctx.socket(zmq.REQ)
    req_socket.connect(endpoint)

    logger.info('client initialized')
    keep_looping = True 
    while keep_looping:
        try:
            req_socket.send(b'CONTACT#....')
            encoded_task = req_socket.recv()
            
            plain_task = encoded_task.decode()  #T_{id:03d}
            sleep(1)  # simulate work : resize, download, upload, summaryze 
            logger.info(f'client has consumed the task {plain_task}')
            
            res = plain_task.split('_')[1][-1::-1]
            response = f'RESPONSE#{res}'
            req_socket.send(response.encode())
            _ = req_socket.recv() # confirmation 
        except KeyboardInterrupt:
            keep_looping = False 
        except Exception as e:
            logger.error(e)

    req_socket.close(linger=0)
    ctx.term() 
    logger.info('client release zeromq resources')

if __name__ == '__main__':
    handler()
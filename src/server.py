

import zmq 
import click 

from src.log import logger 

from typing import List, Any 


@click.command()
@click.option('--endpoint')
@click.option('--nb_tasks', type=int, default=8)
def handler(endpoint:str, nb_tasks:int):
    tasks:List[str] = [ f'T_{i:03d}' for i in range(nb_tasks)]
    accumulator:List[Any] = []
    ctx = zmq.Context()
    rep_socket:zmq.Socket = ctx.socket(zmq.REP)
    rep_socket.bind(endpoint)

    logger.info('server initialized')
    index = 0
    nb_responses = 0
    keep_looping = True 
    while keep_looping:
        try:
            bytestream:bytes = rep_socket.recv()
            key, content = bytestream.split(b'#')
            if key == b'CONTACT':
                current_task = tasks[index]
                rep_socket.send(current_task.encode())
                index = index + 1 
            if key == b'RESPONSE':
                accumulator.append(content) 
                rep_socket.send(b'OK')  # send confirmation 
                nb_responses += 1 
            keep_looping = nb_responses < len(tasks) 
        except KeyboardInterrupt:
            keep_looping = False 
        except Exception as e:
            logger.error(e)
    
    print(accumulator)
    rep_socket.close(linger=0)
    ctx.term() 
    logger.info('server released ressources')

if __name__ == '__main__':
    handler()
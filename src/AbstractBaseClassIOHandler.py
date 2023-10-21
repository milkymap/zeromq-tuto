import zmq 

import operator as op 

from threading import Thread, Event, Lock 
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, Optional
from src.log import logger 

class ABCZmqIOHandler(ABC):
    def __init__(self):
        pass 
    
    @abstractmethod
    def map_task(self, task:str) -> Any:
        pass 

    def __map_task(self, task:str) -> Tuple[bool, Any]:
        try:
            response = self.map_task(task)
            return True, response 
        except Exception as e:
            logger.error(e)
        
        return False, None 
    
    def __create_socket(self, socket_type:str):
        pass 
    
    def __worker(self):
        pass 

    def __source(self):
        pass 

    def __target(self):
        pass 

    def __enter__(self):
        self.ctx = zmq.Context()
        return self 

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.warning(exc_value)
            logger.exception(traceback)
        self.ctx.term()

"""
    REQ/REP
    DEALER/ROUTER
    PUSH/PULL
    PUB/SUB
    PAIR

    tasks : List[str] = [t0, t1, ..., tm]
    for task in tasks:
        process(task)
    
          ventilator
              |
              |
              |
       ---------------
       |      |      |
    worker worker worker  : map : t_i => r_i 
       |      |      |
       |      |      |
       ---------------
              |
              |
             sink : [r0, r1, ..., rm] => RES

"""
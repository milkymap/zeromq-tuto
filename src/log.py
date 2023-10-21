import logging 

logging.basicConfig(
    format='%(asctime)s - %(filename)s - %(lineno)3d - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(name='zmq-handler')

if __name__ == '__main__':
    logger.debug('log initialized')
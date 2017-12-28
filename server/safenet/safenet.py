import logging, time
from threading import Thread
import restapi, mqtt_client
from logging.config import fileConfig
import mqtt_config

fileConfig('logging_config.ini')
logger = logging.getLogger()

mqtt_broker_ip = mqtt_config.mqtt['broker_ip']
mqtt_broker_port = mqtt_config.mqtt['broker_port']
mqtt_broker_username = mqtt_config.mqtt['broker_username']
mqtt_broker_password = mqtt_config.mqtt['broker_password']

def run() :
    logger.info("Starting SafeNet app %s......", time.asctime())

    try:
        restapi_thread = Thread(target=restapi.start_restapi, args=())
        restapi_thread.daemon = True


        mqtt_thread = Thread(target=mqtt_client.connect, args=(mqtt_broker_ip, mqtt_broker_port, mqtt_broker_username, mqtt_broker_password))
        mqtt_thread.daemon = True


        restapi_thread.start()
        mqtt_thread.start()
        restapi_thread.join()
        mqtt_thread.join()
    except Exception, errtxt:
        logger.error("There was an exception while trying to start application: ", errtxt)
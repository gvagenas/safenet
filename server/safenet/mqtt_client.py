import paho.mqtt.client as paho
import json

import sys

import handle_mac_addr
import logging as logger
import mqtt_config

topic = mqtt_config.mqtt['topic']

#Method to executed on succesfull connect to MQTT broker
def on_connect(client, userdata, flags, rc):
    logger.info("CONNACK received with code %d.", (rc))
    client.subscribe(topic, qos=1)
    logger.info("Mqtt client connected and subscribed to topic: %s ", topic)
    handle_mac_addr.start_work()


def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

#Method to execute when succesfully subscribed to a topic
def on_subscribe(client, userdata, mid, granted_qos):
    logger.info("Subscribed: "+str(mid)+" "+str(granted_qos))

#Method to execute when receive a message on subscribed topic
def on_message(client, userdata, msg):
    # print("Topic: "+msg.topic+", QoS: "+str(msg.qos)+", Payload: "+str(msg.payload))
    handle_payload(msg.topic, msg.payload.decode('utf-8'))

#Method to handle MQTT message payload
def handle_payload(topic, payload):
    # logger.info('Payload: %s' % payload[0:])
    try:
        parsed_json = json.loads(payload)
        logger.info('JSON Object: %s', str(parsed_json))
        handle_mac_addr.handle_mac(parsed_json['mac_addr'], parsed_json['chip_id'], parsed_json['location'].split(":")[0])
    except Exception, errtxt:
        logger.error("Exception while trying to parse mqtt payload, exception %s, payload %s", errtxt, payload)


def connect(mqtt_broker_ip, mqtt_broker_port, mqtt_broker_username, mqtt_broker_password):
    logger.info("About to start MQTT Client and connect to \"%s:%s\"", mqtt_broker_ip,mqtt_broker_port)
    client = paho.Client(client_id="safenetserver", clean_session=True, userdata=None, protocol=paho.MQTTv31)

    client.username_pw_set(mqtt_broker_username, mqtt_broker_password)

    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_connect = on_connect
    try:
        client.connect(mqtt_broker_ip, mqtt_broker_port, keepalive=60)
        client.loop_forever()
    except Exception, errtxt:
        logger.error("Exception while trying to connect to MQTT broker, will quit app, exception %s", errtxt)



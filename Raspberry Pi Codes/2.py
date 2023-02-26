# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 21:29:54 2020

@author: Anand
"""
import paho.mqtt.client as mqtt
import os
import time

HOST = '172.18.0.4'
PORT = 1883
MQTT_TOPIC = [("DIAL/Accel-x",0),("DIAL/Accel-y",0),("DIAL/Accel-z",0),("DIAL/Gyro-x",0),("DIAL/Gyro-y",0),("DIAL/Gyro-z",0),("DIAL/InTemperature",0),("DIAL/Temperature",0),("DIAL/humidity",0),("DIAL/irms",0),("DIAL/power",0)]
#MQTT_TOPIC=[("DIAL/192.168.1.24/Temperature",0)]

def fmtRESTapi(topc, mesg):
    dev=topc.split("/")[0]
    loc=topc.split("/")[1]
    var="curl -i -XPOST 'http://172.18.0.2:8086/write?db=iot' --data-binary '"+dev+" "+loc+"="+mesg+"'"
    # print(var)
    os.system(var)

def rest_api(topc, load):
    msg=str(load.decode("utf-8"))
    top=str(topc)
    print("message: ", msg)
    print("topic: ", top)
    fmtRESTapi(top,msg)


def on_connect(client, userdata, flags, rc):
    # Subscribe to any topic starting with 'hermes/intent/'
    # client.subscribe('DIAL/192.168.1.23/Irms')
    client.subscribe(MQTT_TOPIC)
    
    

def on_message(client, userdata, msg):
    print("Message received on topic {0}: {1}"\
        .format(msg.topic, msg.payload))
    rest_api(msg.topic, msg.payload)
    
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, 60)
client.loop_forever()
    

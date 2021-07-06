#!/usr/bin/env python3
'''
Pulls in stats from the CHIP environment on a regular basis.

'''
import os
import subprocess
import signal
import sys
import time
import paho.mqtt.publish as publish
import settings
import socket
import shutil

# Use signal to shutdown
def shutdown(signum, frame):
    battery.send_signal(9)
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

# Common paths
battery_cmd = '/usr/bin/battery.sh'
cpu_cmd = ['/usr/bin/top','-bn 1','-p 0']

# Setup MQTT authentication if used
mqttauth = None
if len(settings.MQTT_USER) and len(settings.MQTT_PASSWORD):
	mqttauth = {'username':settings.MQTT_USER, 'password':settings.MQTT_PASSWORD}

# Setup hostname variable, which will be the topic of the MQTT message
hostname = None
if len(settings.HOSTNAME):
    hostname = settings.HOSTNAME
else:
    hostname = socket.gethostname()

# Send data to MQTT broker
def send_mqtt(topic, payload,):
    try:
        publish.single(topic, payload=payload, qos=1, hostname=settings.MQTT_HOST, port=settings.MQTT_PORT, auth=mqttauth)
    except Exception as ex:
        print('MQTT Publish Error: ' + str(ex))

# Start program loop
while True:
    try:
        # Process and report on battery stats
        if settings.STAT_BATTERY:
            battery = subprocess.Popen(battery_cmd, stdout=subprocess.PIPE, universal_newlines=True)
            for line in battery.stdout:
                if not line:
                    break
                # Remove spaces and split the value at =
                value = line.replace(' = ','=').replace(' ','_').split('=')
                if settings.CLEAN_VALUES:
                    # Remove units to make them integers
                    value[1] = value[1].replace('mA','').replace('c','').replace('mV','')
                send_mqtt('chip/{}/battery/{}'.format(hostname, value[0].lower()), value[1])

        # Process and report on disk stats
        if settings.STAT_DISK:
            total, used, free = shutil.disk_usage("/")
            send_mqtt('chip/{}/disk/total'.format(hostname), round(total/1024/1024, 2))
            send_mqtt('chip/{}/disk/used'.format(hostname), round(used/1024/1024, 2))
            send_mqtt('chip/{}/disk/free'.format(hostname), round(free/1024/1024, 2))

        # Process and report on CPU and RAM stats
        if settings.STAT_CPUMEM:
            cpu = subprocess.Popen(cpu_cmd, stdout=subprocess.PIPE, universal_newlines=True)
            cpu_load_lines = cpu.stdout.readlines()
            cpu_load = cpu_load_lines[2].split(' ')
            send_mqtt('chip/{}/cpu/usage'.format(hostname), cpu_load[1])
            mem_info = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
            send_mqtt('chip/{}/mem/mem_total'.format(hostname), mem_info['MemTotal'])
            send_mqtt('chip/{}/mem/mem_free'.format(hostname), mem_info['MemFree'])

        # Pause until the next time
        time.sleep(settings.FREQUENCY)


    except Exception as e:
        print('Error! {}: {}', e.__class__.__name__, e)
        time.sleep(2)

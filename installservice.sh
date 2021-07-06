#!/bin/bash

cp /opt/chip2mqtt/chip2mqtt.systemd.service /etc/systemd/system/chip2mqtt.service
systemctl daemon-reload
systemctl enable chip2mqtt.service
service chip2mqtt start

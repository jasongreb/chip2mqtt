# MQTT Server settings
## MQTT_HOST = (string) IP address of your MQTT server
## MQTT_PORT = (int) port number of your MQTT server
## MQTT_USER = (string) username for MQTT server
## MQTT_PASSWORD = (string) password for MQTT server
## If authentication is not needed, leave MQTT_USER and MQTT_PASSWORD as empty strings
MQTT_HOST = ''
MQTT_PORT = 1883
MQTT_USER = ''
MQTT_PASSWORD = ''

# Custom hostname of your machine. Leave empty to pull the system hostname.
HOSTNAME = ''

# How often to check and publish settings in seconds
FREQUENCY = 60

# Set to false if you want to leave the values on temp and voltages
CLEAN_VALUES = True

# Set the values to the stats you want to report on
## Battery is output from battery.sh
## Disk size reported in MB
## CPU (in progress)
STAT_BATTERY = True
STAT_DISK = True
STAT_CPUMEM = True